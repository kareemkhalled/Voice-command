import pymongo
from pymongo import DESCENDING
import numpy as np
from datetime import datetime, timedelta

def connect_to_mongodb(uri, db_name, collection_name):
    client = pymongo.MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection

def get_documents_between_dates(collection, start_date, end_date):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) 
    
    query = {
        "updated_at": {
            "$gte": str(start_datetime) + "00:00:00.000000+00:00",
            "$lt": str(end_datetime) + "00:00:00.000000+00:00"
        }
    }
    
    documents = collection.find(query)
    return list(documents)

def get_last_document_for_date(collection, date):
    date_datetime = datetime.strptime(date, "%Y-%m-%d")
    next_date_datetime = date_datetime + timedelta(days=1) 
    print(date_datetime)
    print(next_date_datetime)
    
    query = {
        "updated_at": {
            "$gte": date_datetime.isoformat() + "T00:00:00.000000+00:00",
            "$lt": next_date_datetime.isoformat() + "T00:00:00.000000+00:00"
        }
    }
    
    last_document = collection.find(query).sort("updated_at", DESCENDING).limit(1)
    print(last_document)
    return last_document[0]
    


def calculate_sums(documents):
    if not documents:
        return {}
    
    data_dict = {}
    for doc in documents:
        for key, value in doc.items():
            if key != "_id" and key != "updated_at" and key != "station_id":
                try:
                    value = float(value)
                    if key in data_dict:
                        data_dict[key].append(value)
                    else:
                        data_dict[key] = [value]
                except ValueError:
                    continue

    sum_dict = {}
    for key, values in data_dict.items():
        values = np.array(values)
        mean = np.mean(values)
        std_dev = np.std(values)
        
        z_scores = np.abs((values - mean) / std_dev)
        filtered_values = values[z_scores < 3]
        
        if filtered_values.size > 0:
            sum_dict[key] = np.sum(filtered_values)
        else:
            sum_dict[key] = None  

    return sum_dict

def calculate_averages(documents):
    if not documents:
        return {}
    
    data_dict = {}
    avg_dict = {}
    for doc in documents:
        for key, value in doc.items():
            if key != "_id" and key != "updated_at" and key != "station_id" and 'on' not in key.lower() and 'off' not in key.lower() :
                try:
                    value = float(value)
                    if key in data_dict:
                        data_dict[key].append(value)
                    else:
                        data_dict[key] = [value]
                except ValueError:
                    continue
            else:
                avg_dict[key] = value
            
    for key, values in data_dict.items():
        values = np.array(values)
        mean = np.mean(values)
        std_dev = np.std(values)
        
        z_scores = np.abs((values - mean) / std_dev)
        filtered_values = values[z_scores < 3]
        
        if filtered_values.size > 0:
            avg_dict[key] = round(float(np.mean(filtered_values)), 1)
        else:
            avg_dict[key] = None  

    return avg_dict
  

def main():
    uri = "mongodb://root:ZZ4P6ePRfmmL8Z()3aFk@localhost:27017/"  
    db_name = "stations"  
    collection_name = "5"  
    
    collection = connect_to_mongodb(uri, db_name, collection_name)
    
    start_date = "2024-10-08"
    end_date = "2024-10-17"
    
    documents = get_documents_between_dates(collection, start_date, end_date)
    print(documents)
    averages = calculate_averages(documents)
    
    for key, value in averages.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
