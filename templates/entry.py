import csv
from sqlalchemy import create_engine, Column, Integer,Float, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define your SQLAlchemy model
Base = declarative_base()
class ValidData(Base):
    __tablename__ = 'VALUES'
    place = Column(String(80), primary_key=True)
    state = Column(String(80), primary_key=True)
    lat = Column(Float, unique=False, nullable=False)
    lon  = Column(Float, unique=False, nullable=False)
    power = Column(Float, unique=False, nullable=False)
    ws  = Column(Float, unique=False, nullable=False)
    wd = Column(Float, unique=False, nullable=False)


# Create a connection to the database and a session
engine = create_engine('sqlite:///new.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Read the CSV file and insert rows into the database
csv_file_path = 'NewData.csv'
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        new_row = ValidData(place=row['LOCATION_NAME'], state = row['REGION'],lat = row['LATITUDE'],lon= row['LONGITUDE'],power= row['POW'],ws= row['WIND SPEED'],wd= row['WIND DIRECTION'])
        session.add(new_row)

# Commit the changes to the database
session.commit()

# Close the session
session.close()
