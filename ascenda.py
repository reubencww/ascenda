
#
# Complete the 'merchant_offers' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING checkin
#  2. STRING offers_json
#
import json
import copy
from datetime import datetime, timedelta

def remove_invalid_offers(checkin, offers):
    '''
    Function to filter offers based on category and their required rules
    Restaurant: The offer is valid until the check-in date plus 3 days.
    Retail: The offer is valid until the check-in date plus 5 days.
    Activity: The offer is valid until the check-in date plus 7 days.
    '''
    checkin_dt = datetime.strptime(checkin, "%Y-%m-%d")
    filtered_offers = []

    for offer in offers:
        valid_to_dt = datetime.strptime(offer["valid_to"], "%Y-%m-%d")
        match offer['category']:
            case 1:
                # Resturant
                if checkin_dt + timedelta(days=3) <= valid_to_dt:
                    filtered_offers.append(offer)
            case 2: 
                # Retail
                if checkin_dt + timedelta(days=5) <= valid_to_dt:
                    filtered_offers.append(offer)
            case 4:
                # Activity
                if checkin_dt + timedelta(days=7) <= valid_to_dt:
                    filtered_offers.append(offer)
            case _:
                continue

    return filtered_offers

def get_min_merchant(merchant):
    return merchant['distance']

def get_min_distance_for_each_cat(offers):
    '''
    Function to sort offers based on their distance, incrementally
    '''
    copied_offers = offers

    for offer in copied_offers:
      offer["merchants"] = min(offer["merchants"], key = get_min_merchant)

    sorted_offers = sorted(copied_offers, key = lambda offer: (offer["merchants"]["distance"]))
    return sorted_offers

def get_sorted_offers_with_score(offers, age_group, gender):
    '''
    Function to sort offers by highest scores
    '''
    age_score = 1.25
    gender_score = 1.5
    copied_offers = offers

    for offer in copied_offers:
        offer["gender_scores"] = offer["gender_scores"][gender] * gender_score
        offer["age_scores"] = offer["age_scores"][age_group] * age_score
    
    sorted_offers = sorted(copied_offers, key = lambda offer: (offer["gender_scores"] + offer["age_scores"]), reverse=True)
    return sorted_offers

def format_offer(offer):
    match offer["category"]:
        case 1:
            return {
                "id": offer["id"],
                "title": offer["title"],
                "description": offer["description"],
                "category": "Restaurant"
            }
        case 2:
            return {
                "id": offer["id"],
                "title": offer["title"],
                "category": "Retail"
            }
        case 4:
            return {
                "id": offer["id"],
                "title": offer["title"],
                "description": offer["description"],
                "valid_to": offer["valid_to"],
                "category": "Activity",
            }
    

def get_best_offers(offers):
    '''
    Function to get 2 offers of different categories
    '''
    have_category = None
    ret = []

    for offer in offers:
        filtered_offer = format_offer(offer)
        if have_category == None:
            # no offers taken
            ret.append(filtered_offer)

            have_category = offer['category']
            continue
        if have_category == offer['category']:
            continue
        ret.append(filtered_offer)
        break
    return ret        

def merchant_offers(checkin, offers_json, age_group, gender):
    '''
    Function to filter and get best offers
    '''
        
    valid_offers = remove_invalid_offers(checkin, offers_json)
    offers_with_score = get_sorted_offers_with_score(valid_offers, age_group, gender)
    cat_offers_min_distance = get_min_distance_for_each_cat(offers_with_score)
    best_offers = get_best_offers(cat_offers_min_distance)

    return best_offers

if __name__ == '__main__':
    
  with open('offers.json', 'r') as f:
    data = json.load(f)



  # print(merchant_offers('2023-05-22', copy.deepcopy(data)))
  # print(merchant_offers('2023-05-20', copy.deepcopy(data)))
  # print(merchant_offers('2023-05-18', copy.deepcopy(data)))
  # print(merchant_offers('2023-05-15', copy.deepcopy(data)))

  # print(merchant_offers('2023-05-15', copy.deepcopy(data), 'young_adults', 'male'))   # [3, 6]
  # print(merchant_offers('2023-05-15', copy.deepcopy(data), 'teens', 'male'))          # [3, 2]
  # print(merchant_offers('2023-05-15', copy.deepcopy(data), 'seniors', 'male'))        # [2, 3]
    
  print(merchant_offers('2023-05-15', copy.deepcopy(data), 'young_adults', 'male'))     # [{'id': 3, 'title': 'Offer 3', 'description': 'Offer 3 description', 'valid_to': '2023-05-24', 'category': 'Activity'}, {'id': 6, 'title': 'Offer 6', 'category': 'Retail'}]
