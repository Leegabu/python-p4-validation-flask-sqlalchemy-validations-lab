from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError("Name cannot be empty.")        
    
        existing_auth=Author.query.filter(Author.name==name).first()
        if existing_auth and existing_auth.id != self.id:
            raise ValueError("Name has already been taken.Enter a unique name.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number has to be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self,key,content):
        if len(content)>= 250:
            return content
        else:
            raise ValueError("Post content is at least 250 characters long.")
    @validates('summary')
    def validate_summary(self,key,summary):
        if len(summary)<=250:
            return summary
        else:
            raise ValueError("Post summary is a maximum of 250 characters.")
    @validates('category')
    def validate_category(self,key,category):
        if category not in ['Fiction','Non-Fiction']:
            raise ValueError("Post Category  must either be Fiction or Non-Fiction ")
        return category
    @validates('title')
    def validate_title(self,key,title):
        if  not any (phrase in title for phrase in ["Won't Believe","Secret","Top","Guess"]):
            raise ValueError("Title has to contain one of the following:'Won't' 'Believe','Secret','Top','Guess'")
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
