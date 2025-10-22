from neo4j import GraphDatabase
from typing import Optional, List, Dict
import uuid
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

class Neo4jConnection:
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self.max_connection_lifetime = 3600  # 1 hour
        self.connection_timeout = 60  # Increased from 30 to 60 seconds
        self.max_retry_attempts = 5  # Increased from 3 to 5
        self.retry_delay = 2  # Increased from 1 to 2 seconds

    def connect(self):
        """Connect to Neo4j with proper configuration for Aura"""
        try:
            # Configure driver for Neo4j Aura with connection pooling
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                max_connection_lifetime=self.max_connection_lifetime,
                max_connection_pool_size=10,
                connection_timeout=self.connection_timeout,
                connection_acquisition_timeout=120,  # Increased from 60 to 120 seconds
                # Note: trusted_certificates not needed with neo4j+s:// scheme
            )
            logger.info("Neo4j driver configured for Aura")

            # Don't test connection immediately - let it be lazy
            # Connection will be tested when first used

        except Exception as e:
            logger.error(f"Failed to create Neo4j driver: {e}")
            self.driver = None
            raise

    def close(self):
        """Close the Neo4j driver"""
        if self.driver:
            self.driver.close()

    def _execute_with_retry(self, operation, *args, **kwargs):
        """Execute database operation with retry logic"""
        for attempt in range(self.max_retry_attempts):
            try:
                return operation(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Database operation failed (attempt {attempt + 1}/{self.max_retry_attempts}): {e}")

                if attempt < self.max_retry_attempts - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Database operation failed after {self.max_retry_attempts} attempts")

        # This should never be reached, but just in case
        raise Exception("Database operation failed after all retry attempts")

    def _convert_neo4j_types(self, data):
        """Convert Neo4j types to standard Python types for JSON serialization"""
        if isinstance(data, dict):
            return {key: self._convert_neo4j_types(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._convert_neo4j_types(item) for item in data]
        elif hasattr(data, '__class__') and 'neo4j.time' in str(data.__class__):
            # Convert Neo4j datetime objects to Python datetime
            return data.to_native()
        else:
            return data

    def create_constraints(self):
        """Create database constraints with error handling and retry logic"""
        def _create_constraints_internal():
            with self.driver.session() as session:
                # Create unique constraints
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (r:Room) REQUIRE r.id IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (b:Booking) REQUIRE b.id IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tenant) REQUIRE t.id IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Notification) REQUIRE n.id IS UNIQUE")

        try:
            self._execute_with_retry(_create_constraints_internal)
        except Exception as e:
            logger.warning(f"Could not create database constraints: {e}")
            # Don't raise the exception - allow app to continue

    def create_user(self, email: str, username: str, password: str, role: str = "user") -> str:
        def _create_user_internal():
            with self.driver.session() as session:
                user_id = str(uuid.uuid4())
                # Hash the password before storing
                from auth import get_password_hash
                hashed_password = get_password_hash(password)

                query = """
                CREATE (u:User {
                    id: $id,
                    email: $email,
                    username: $username,
                    password: $password,
                    role: $role,
                    created_at: datetime()
                })
                RETURN u.id as id
                """
                result = session.run(query, id=user_id, email=email, username=username,
                                   password=hashed_password, role=role)
                return result.single()["id"]

        try:
            return self._execute_with_retry(_create_user_internal)
        except Exception as e:
            logger.error(f"Database error in create_user: {e}")
            # Check if it's a constraint violation (duplicate email)
            if "ConstraintValidationFailed" in str(e) or "already exists" in str(e):
                raise Exception("User with this email already exists")
            raise Exception("Database connection unavailable. Please try again later.")

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        def _get_user_internal():
            with self.driver.session() as session:
                query = "MATCH (u:User {email: $email}) RETURN u"
                result = session.run(query, email=email)
                record = result.single()
                if record:
                    return self._convert_neo4j_types(dict(record["u"]))
                return None

        try:
            return self._execute_with_retry(_get_user_internal)
        except Exception as e:
            logger.error(f"Database error in get_user_by_email: {e}")
            return None

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        def _get_user_by_id_internal():
            with self.driver.session() as session:
                query = "MATCH (u:User {id: $id}) RETURN u"
                result = session.run(query, id=user_id)
                record = result.single()
                if record:
                    return self._convert_neo4j_types(dict(record["u"]))
                return None

        try:
            return self._execute_with_retry(_get_user_by_id_internal)
        except Exception as e:
            logger.error(f"Database error in get_user_by_id: {e}")
            return None

    def create_room(self, room_number: str, room_type: str, capacity: int,
                   price: float, status: str = "available") -> str:
        def _create_room_internal():
            with self.driver.session() as session:
                room_id = str(uuid.uuid4())
                query = """
                CREATE (r:Room {
                    id: $id,
                    room_number: $room_number,
                    room_type: $room_type,
                    capacity: $capacity,
                    price: $price,
                    status: $status,
                    created_at: datetime()
                })
                RETURN r.id as id
                """
                result = session.run(query, id=room_id, room_number=room_number,
                                   room_type=room_type, capacity=capacity,
                                   price=price, status=status)
                return result.single()["id"]

        try:
            return self._execute_with_retry(_create_room_internal)
        except Exception as e:
            logger.error(f"Database error in create_room: {e}")
            raise Exception("Database connection unavailable. Please try again later.")

    def get_all_rooms(self) -> List[Dict]:
        def _get_all_rooms_internal():
            with self.driver.session() as session:
                query = "MATCH (r:Room) RETURN r ORDER BY r.room_number"
                result = session.run(query)
                return [self._convert_neo4j_types(dict(record["r"])) for record in result]

        try:
            return self._execute_with_retry(_get_all_rooms_internal)
        except Exception as e:
            logger.error(f"Database error in get_all_rooms: {e}")
            return []

    def get_room_by_id(self, room_id: str) -> Optional[Dict]:
        def _get_room_internal():
            with self.driver.session() as session:
                query = "MATCH (r:Room {id: $id}) RETURN r"
                result = session.run(query, id=room_id)
                record = result.single()
                if record:
                    return self._convert_neo4j_types(dict(record["r"]))
                return None

        try:
            return self._execute_with_retry(_get_room_internal)
        except Exception as e:
            logger.error(f"Database error in get_room_by_id: {e}")
            return None

    def update_room(self, room_id: str, updates: Dict):
        def _update_room_internal():
            with self.driver.session() as session:
                set_clause = ", ".join([f"r.{key} = ${key}" for key in updates.keys()])
                query = f"MATCH (r:Room {{id: $id}}) SET {set_clause} RETURN r"
                session.run(query, id=room_id, **updates)

        try:
            self._execute_with_retry(_update_room_internal)
        except Exception as e:
            logger.error(f"Database error in update_room: {e}")
            raise

    def delete_room(self, room_id: str):
        def _delete_room_internal():
            with self.driver.session() as session:
                query = "MATCH (r:Room {id: $id}) DETACH DELETE r"
                session.run(query, id=room_id)

        try:
            self._execute_with_retry(_delete_room_internal)
        except Exception as e:
            logger.error(f"Database error in delete_room: {e}")
            raise

    def create_booking(self, user_id: str, room_id: str, start_date: str,
                      end_date: str, duration: int) -> str:
        def _create_booking_internal():
            with self.driver.session() as session:
                booking_id = str(uuid.uuid4())
                query = """
                MATCH (u:User {id: $user_id}), (r:Room {id: $room_id})
                CREATE (b:Booking {
                    id: $id,
                    start_date: $start_date,
                    end_date: $end_date,
                    duration: $duration,
                    status: $status,
                    created_at: datetime()
                })
                CREATE (u)-[:MADE_BOOKING]->(b)
                CREATE (b)-[:FOR_ROOM]->(r)
                RETURN b.id as id
                """
                result = session.run(query, id=booking_id, user_id=user_id,
                                   room_id=room_id, start_date=start_date,
                                   end_date=end_date, duration=duration, status="pending")
                return result.single()["id"]

        try:
            return self._execute_with_retry(_create_booking_internal)
        except Exception as e:
            logger.error(f"Database error in create_booking: {e}")
            raise Exception("Database connection unavailable. Please try again later.")

    def get_user_bookings(self, user_id: str) -> List[Dict]:
        def _get_user_bookings_internal():
            with self.driver.session() as session:
                query = """
                MATCH (u:User {id: $user_id})-[:MADE_BOOKING]->(b:Booking)-[:FOR_ROOM]->(r:Room)
                RETURN b, r
                ORDER BY b.created_at DESC
                """
                result = session.run(query, user_id=user_id)
                bookings = []
                for record in result:
                    booking = self._convert_neo4j_types(dict(record["b"]))
                    booking["room"] = self._convert_neo4j_types(dict(record["r"]))
                    bookings.append(booking)
                return bookings

        try:
            return self._execute_with_retry(_get_user_bookings_internal)
        except Exception as e:
            logger.error(f"Database error in get_user_bookings: {e}")
            return []

    def get_booking_by_id(self, booking_id: str) -> Optional[Dict]:
        def _get_booking_internal():
            with self.driver.session() as session:
                query = """
                MATCH (u:User)-[:MADE_BOOKING]->(b:Booking {id: $id})-[:FOR_ROOM]->(r:Room)
                RETURN b, r, u.id as user_id
                """
                result = session.run(query, id=booking_id)
                record = result.single()
                if record:
                    booking = self._convert_neo4j_types(dict(record["b"]))
                    booking["room"] = self._convert_neo4j_types(dict(record["r"]))
                    booking["user_id"] = record["user_id"]
                    return booking
                return None

        try:
            return self._execute_with_retry(_get_booking_internal)
        except Exception as e:
            logger.error(f"Database error in get_booking_by_id: {e}")
            return None

    def update_booking(self, booking_id: str, updates: Dict):
        def _update_booking_internal():
            with self.driver.session() as session:
                set_clause = ", ".join([f"b.{key} = ${key}" for key in updates.keys()])
                query = f"MATCH (b:Booking {{id: $id}}) SET {set_clause} RETURN b"
                session.run(query, id=booking_id, **updates)

        try:
            self._execute_with_retry(_update_booking_internal)
        except Exception as e:
            logger.error(f"Database error in update_booking: {e}")
            raise

    def create_tenant(self, name: str, email: str, phone: str, room_id: str) -> str:
        def _create_tenant_internal():
            with self.driver.session() as session:
                tenant_id = str(uuid.uuid4())
                query = """
                MATCH (r:Room {id: $room_id})
                CREATE (t:Tenant {
                    id: $id,
                    name: $name,
                    email: $email,
                    phone: $phone,
                    created_at: datetime()
                })
                CREATE (t)-[:OCCUPIES]->(r)
                RETURN t.id as id
                """
                result = session.run(query, id=tenant_id, name=name, email=email,
                                   phone=phone, room_id=room_id)
                return result.single()["id"]

        try:
            return self._execute_with_retry(_create_tenant_internal)
        except Exception as e:
            logger.error(f"Database error in create_tenant: {e}")
            raise Exception("Database connection unavailable. Please try again later.")

    def get_all_tenants(self) -> List[Dict]:
        def _get_all_tenants_internal():
            with self.driver.session() as session:
                query = """
                MATCH (t:Tenant)-[:OCCUPIES]->(r:Room)
                RETURN t, r
                ORDER BY t.name
                """
                result = session.run(query)
                tenants = []
                for record in result:
                    tenant = self._convert_neo4j_types(dict(record["t"]))
                    tenant["room"] = self._convert_neo4j_types(dict(record["r"]))
                    tenants.append(tenant)
                return tenants

        try:
            return self._execute_with_retry(_get_all_tenants_internal)
        except Exception as e:
            logger.error(f"Database error in get_all_tenants: {e}")
            return []

    def create_notification(self, user_id: str, booking_id: str,
                          message: str, notification_type: str) -> str:
        def _create_notification_internal():
            with self.driver.session() as session:
                notification_id = str(uuid.uuid4())
                query = """
                MATCH (u:User {id: $user_id}), (b:Booking {id: $booking_id})
                CREATE (n:Notification {
                    id: $id,
                    message: $message,
                    type: $type,
                    status: $status,
                    created_at: datetime()
                })
                CREATE (n)-[:FOR_USER]->(u)
                CREATE (n)-[:ABOUT_BOOKING]->(b)
                RETURN n.id as id
                """
                result = session.run(query, id=notification_id, user_id=user_id,
                                   booking_id=booking_id, message=message,
                                   type=notification_type, status="pending")
                return result.single()["id"]

        try:
            return self._execute_with_retry(_create_notification_internal)
        except Exception as e:
            logger.error(f"Database error in create_notification: {e}")
            raise Exception("Database connection unavailable. Please try again later.")

    def get_all_notifications(self) -> List[Dict]:
        def _get_all_notifications_internal():
            with self.driver.session() as session:
                query = """
                MATCH (n:Notification)-[:FOR_USER]->(u:User)
                OPTIONAL MATCH (n)-[:ABOUT_BOOKING]->(b:Booking)
                RETURN n, u, b
                ORDER BY n.created_at DESC
                """
                result = session.run(query)
                notifications = []
                for record in result:
                    notif = self._convert_neo4j_types(dict(record["n"]))
                    notif["user"] = self._convert_neo4j_types(dict(record["u"]))
                    if record["b"]:
                        notif["booking_id"] = dict(record["b"])["id"]
                    notifications.append(notif)
                return notifications

        try:
            return self._execute_with_retry(_get_all_notifications_internal)
        except Exception as e:
            logger.error(f"Database error in get_all_notifications: {e}")
            return []

    def get_user_notifications(self, user_id: str) -> List[Dict]:
        def _get_user_notifications_internal():
            with self.driver.session() as session:
                query = """
                MATCH (n:Notification)-[:FOR_USER]->(u:User {id: $user_id})
                OPTIONAL MATCH (n)-[:ABOUT_BOOKING]->(b:Booking)
                RETURN n, b
                ORDER BY n.created_at DESC
                """
                result = session.run(query, user_id=user_id)
                notifications = []
                for record in result:
                    notif = self._convert_neo4j_types(dict(record["n"]))
                    if record["b"]:
                        notif["booking_id"] = dict(record["b"])["id"]
                    notifications.append(notif)
                return notifications

        try:
            return self._execute_with_retry(_get_user_notifications_internal)
        except Exception as e:
            logger.error(f"Database error in get_user_notifications: {e}")
            return []

    def get_notification_by_id(self, notification_id: str) -> Optional[Dict]:
        def _get_notification_internal():
            with self.driver.session() as session:
                query = """
                MATCH (n:Notification {id: $id})
                OPTIONAL MATCH (n)-[:ABOUT_BOOKING]->(b:Booking)
                RETURN n, b.id as booking_id
                """
                result = session.run(query, id=notification_id)
                record = result.single()
                if record:
                    notif = self._convert_neo4j_types(dict(record["n"]))
                    if record["booking_id"]:
                        notif["booking_id"] = record["booking_id"]
                    return notif
                return None

        try:
            return self._execute_with_retry(_get_notification_internal)
        except Exception as e:
            logger.error(f"Database error in get_notification_by_id: {e}")
            return None

    def update_notification(self, notification_id: str, updates: Dict):
        def _update_notification_internal():
            with self.driver.session() as session:
                set_clause = ", ".join([f"n.{key} = ${key}" for key in updates.keys()])
                query = f"MATCH (n:Notification {{id: $id}}) SET {set_clause} RETURN n"
                session.run(query, id=notification_id, **updates)

        try:
            self._execute_with_retry(_update_notification_internal)
        except Exception as e:
            logger.error(f"Database error in update_notification: {e}")
            raise
