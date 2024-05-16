from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, or_
from sqlalchemy.orm import relationship
from app import Base, session

# User Profile Class
class UserProfile(Base):
    __tablename__ = "user_profile"
    
    profile_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    roles = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)
    suspend_status = Column(Boolean, nullable=False)
    user = relationship("User", back_populates="userprofile")

    # Constructor
    def __init__(self, roles, description=None):
        #self.profile_id = profile_id
        self.roles = roles
        self.description = description
        self.suspend_status = False

    # Get methods
    def get_profile_id(self):
        return self.profile_id
    
    def get_role(self):
        return self.roles
    
    def get_description(self):
        return self.description
    
    def get_suspend_status(self):
        return self.suspend_status
    
    # Set methods
    def set_profile_id(self, id):
        self.profile_id = id

    def set_role(self, role):
        self.roles = role

    def set_description(self, description):
        self.description = description

    def set_suspend_status(self, status):
        self.suspend_status = status

    # Function to create new profile record in DB
    @classmethod
    def create_new_profile(cls, profile):
        try:
            #with session.begin():
                session.add(profile)
                session.commit()
                session.close()
                return True
        except Exception as e:
            session.rollback()
            print(f"Error creating new profile: {e}")
            session.close()
            return False
                    
    # Function to retrieve all profile records
    @classmethod
    def get_all_profiles(cls):
        profiles = session.query(cls).filter(cls.suspend_status==False).all()
        return profiles

    # Function to retrieve one profile record using profile name
    @classmethod
    def get_profile_by_name(cls, name):
        profile = session.query(cls).filter(cls.roles==name).first()
        return profile

    # Function to update profile information
    @classmethod
    def update_profile(cls, current_role, name, description):
        try:
            profile = session.query(cls).filter(cls.roles==current_role).first()
            profile.set_role(name)
            profile.set_description(description)
            session.commit()
            session.close()
            return True
        
        except Exception as e:
            session.rollback()
            print(f"Error updating profile: {e}")
            session.close()
            return False

    # Function to suspend profile
    @classmethod
    def suspend_profile(cls, role):
        try:
            profile = session.query(cls).filter(cls.roles==role).first()
            profile.set_suspend_status(True) 
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error suspending profile: {e}")
            session.close()
            return False

    # Function to search profile
    @classmethod
    def searchProfile(cls, search_term):
        profiles = session.query(cls) \
                    .filter(cls.suspend_status == False) \
                    .filter((cls.profile_id.contains(search_term)) |  cls.roles.contains(search_term) | cls.description.contains(search_term)) \
                    .all()

        return profiles 
                    

# User Class
class User(Base):
    __tablename__ = "users_info"

    user_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    profile_id = Column(Integer, ForeignKey('user_profile.profile_id'))
    fname = Column(String(255), nullable=False)
    lname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phonenum = Column(String(8), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    suspend_status = Column(Boolean, nullable=False)
    userprofile = relationship("UserProfile", back_populates="user")

    # Constructor
    def __init__(self, profile_id, fname, lname, email, phonenum, username, password_hash):
        self.profile_id = profile_id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phonenum = phonenum
        self.username = username
        self.password_hash = password_hash
        self.suspend_status = False

    # Get methods
    def get_user_id(self):
        return self.user_id
    
    def get_profile_id(self):
        return self.profile_id 
    
    def get_fname(self):
        return self.fname
    
    def get_lname(self):
        return self.lname
    
    def get_email(self):
        return self.email
    
    def get_phone_num(self):
        return self.phonenum
    
    def get_username(self):
        return self.username
    
    def get_password_hash(self):
        return self.password_hash
    
    def get_suspend_status(self):
        return self.suspend_status

    # Set methods
    def set_profile_id(self, id):
        self.profile_id = id

    def set_fname(self, name):
        self.fname = name

    def set_lname(self, name):
        self.lname = name

    def set_email(self, email):
        self.email = email

    def set_phone_num(self, phonenum):
        self.phonenum = phonenum

    def set_username(self, username):
        self.username = username

    def set_password_hash(self, pw_hash):
        self.password_hash = pw_hash

    def set_suspend_status(self, status):
        self.suspend_status = status

    # Function to create new account record in DB
    @classmethod
    def create_new_account(cls, account):
        try:
            #with session.begin():
                session.add(account)
                session.commit()
                return True
        except Exception as e:
            session.rollback()
            print(f"Error creating new account: {e}")
            return False
        finally:
            session.close()

    # Function to check email
    @classmethod
    def check_email(cls, email):
        email_exist = session.query(cls).filter(cls.email==email).first() is not None
        return email_exist
    
     # Function to check phone num
    @classmethod
    def check_phonenum(cls, phonenum):
        phone_num_exist = session.query(cls).filter(cls.phonenum==phonenum).first() is not None
        return phone_num_exist
    
    # Function to check username
    @classmethod
    def check_username(cls, username):
        username_exist = session.query(cls).filter(cls.username==username).first() is not None
        return username_exist


    # Function to read all account records in DB
    @classmethod
    def get_all_accounts(cls):
        users=session.query(cls).filter(cls.suspend_status==False).all()
        return users

    # Function to read one account record 
    @classmethod
    def get_account_by_username(cls, username):
        user = session.query(cls).filter(cls.username==username).first()
        return user

    # Function to update account record in DB
    @classmethod
    def update_account(cls, username, new_fname, new_lname, new_email, new_phone_num, new_password_hash):
        try:
            account = session.query(cls).filter(cls.username==username).first()
            if new_fname != "":
                account.set_fname(new_fname)
            if new_lname != "":
                account.set_lname(new_lname)
            if new_email != "":
                account.set_email(new_email)
            if new_phone_num != "":
                account.set_phone_num(new_phone_num)
            if new_password_hash != "":
                account.set_password_hash(new_password_hash)
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # Function to suspend account record 
    @classmethod
    def suspend_account(cls, username):
        try:
            account = session.query(cls).filter(cls.username==username).first()
            account.set_suspend_status(True) 
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # Function to search account
    @classmethod
    def searchAccount(cls, search_term):
        subquery = session.query(UserProfile.profile_id).filter(UserProfile.roles.contains(search_term)).subquery()

        users = session.query(cls) \
                    .filter(cls.suspend_status == False) \
                    .filter(cls.user_id.contains(search_term) |  
                             cls.fname.contains(search_term) | 
                             cls.lname.contains(search_term) | 
                             cls.email.contains(search_term) | 
                             cls.phonenum.contains(search_term) | 
                             cls.username.contains(search_term) | 
                             cls.profile_id.in_(subquery)) \
                    .all()

        return users 
                    

    def __repr__(self):
        return f'User("{self.user_id}","{self.profile_id}""{self.fname}","{self.lname}","{self.email}","{self.username}","{self.phonenum}")'
