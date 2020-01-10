import re
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client['POS']

def Discounts(User_Input):
    disc_find = re.search(r'discounts?|dis?c|disocunt',User_Input,re.I)
    if disc_find:
        disc1_find = re.search(r'vip|associate 10%?|associate10%?|associate 20%?|associate20%?|associate other%?|manual txn%?|manual item%?|item discount|transaction discount|tjx rewards?|plcc|coupon',User_Input,re.I)
        if  disc1_find:

            if disc1_find.group() == "vip":
                db_word = "VIP"
            elif disc1_find.group() in("associate 10","associate 10%","associate10","associate10%"):
                db_word = "Associate 10%"
            elif disc1_find.group() in ("associate 20","associate 20%","associate20","associate20%"):
                db_word = "Associate 20%"
            elif disc1_find.group() in ("associate other", "associate other%"):
                db_word = "Associate Other%"
            elif disc1_find.group() in ("manual txn", "manual txn%","transaction discount"):
                db_word = "Manual Txn% OFF"
            elif disc1_find.group() in ("manual item","manual item%","item discount"):
                db_word = "Manual Item% OFF"
            elif disc1_find.group() in ("tjx rewards","tjx reward","plcc","coupon"):
                db_word = "TJX Rewards Credit Card Coupon"

            disc_adv = re.search(r'values?|default value|maximum value|max value|maximum percent|maximum|apply|steps?|level|type|kind|receipts?|cvar|editable|modify|description',User_Input,re.I)
            if disc_adv:
                if disc_adv.group() in ("value", "values","default value"):
                    u = db.discount.find_one({"name":db_word},{"default value":1,"_id":0})
                    for v in u.values():
                        if v=="no":
                            
                            #print("\nThere is no default value of",db_word,"discount")
                            return "There is no default value of "+ db_word + " discount"
                            
                        else:
                            #print("\nThe default value of", db_word , "discount is",v,"%")
                            return "The default value of "+db_word+" discount is "+ str(v) + "%"
                            
                elif disc_adv.group() in ("maximum value","max value","maximum percent","maximum"):
                    u = db.discount.find_one({"name": db_word}, {"maximum value": 1, "_id": 0})
                    for v in u.values():
                        return "The maximum value of "+db_word+" discount is "+ "{0:.0f}".format(v)+ "%"
                elif disc_adv.group() in ["level", "type","kind"]:
                    u = db.discount.find_one({"name": db_word}, {"level": 1, "_id": 0})
                    for v in u.values():
                        return "The "+db_word+" discount is "+str(v)+" discount"
                elif disc_adv.group()in ("receipt","receipts"):
                    u = db.discount.find_one({"name": db_word}, {"receipt": 1, "_id": 0})
                    for v in u.values():
                        return "The "+db_word+" discount is printed as "+str(v)+" on the receipt"
                elif disc_adv.group() == "cvar":
                    u = db.discount.find_one({"name": db_word}, {"cvar": 1, "_id": 0})
                    for v in u.values():
                        return "The "+db_word+" discount is printed as "+str(v)+" on the CVAR"
                elif disc_adv.group() in("apply","step","steps"):
                    u = db.discount.find_one({"name": db_word}, {"apply": 1, "_id": 0})
                    for v in u.values():
                        return "Follow the below instructions to apply the "+db_word+" discount "+str(v)
                elif disc_adv.group() in ("editable","modify"):
                    u = db.discount.find_one({"name": db_word}, {"editable": 1, "_id": 0})
                    for v in u.values():
                        if v =="no":
                            return "No, we cannot modify the "+db_word+" discount"
                        else:
                            return "Yes, we can modify the "+db_word+" discount"
                else:
                    u = db.discount.find_one({"name": db_word}, {"description": 1, "_id": 0})
                    for v in u.values():
                        return str(v)
            else:
                u = db.discount.find_one({"name": db_word}, {"description": 1, "_id": 0})
                for v in u.values():
                    return str(v)
        elif re.search(r'returns?|returning|returned',User_Input,re.I):
            return "Yes, we can apply discount to the return items but only during the UNRECEIPTED AND UNVERIFIED RETURNS.\n We are not allowed to apply discoun while performing the RECEIPTED RETURN as it will pull out the original sale txn details"
        elif re.search(r'apply discounts?|applicable',User_Input,re.I):
            return "Discounts can be applied on all the items except for Non Merch items like CHARITIES, BAG FEE, SALE OF SVCs etc. "
        elif re.search(r'max|maximum',User_Input,re.I):
            return "Xstore will allow us to apply discount max by 100%"
        elif re.search(r'2 discounts?|two discounts?|(.*) multiple discounts?|same transactions?|same items?|discounts? override|override', User_Input, re.I):
            return "No,We can't apply multiple discounts at the same time on an item. Xstore will override the previous discount with the newly applied discount."
        elif re.search(r'types? of discounts?|many|types?',User_Input,re.I):
            return "There are total 7 types of discounts in Xstore. 6 are transaction level discounts and 1 is an item level discount. Below are the all available discounts:\nAssociate 10%\nAssociate 20%\nAssociate Other%\nVIP\nTJX Rewards Credit card coupon\nManual Txn% off\nManual Item% off"
        else:
            return " Kindly mention the discount name which you are looking for"
    elif re.search(r'AIN|associate identification number|associate number',User_Input,re.I):
        u = db.discount.find_one({"name": "Associate 10%"}, {"AIN": 1, "_id": 0})
        for v in u.values():
            return v
    elif re.search(r'Coupon code|coupon number|5 digit',User_Input,re.I):
        u = db.discount.find_one({"name": "TJX Rewards Credit Card Coupon"}, {"Coupon": 1, "_id": 0})
        for v in u.values():
            return v
    else:
        return "OOPS! We are still in development phase. Kindly ask any query related to DISCOUNT only"


  
    
