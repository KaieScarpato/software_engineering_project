def init_database():
    import openpyxl
    import random
    from ..models import Beer
    from .. import db
    dataframe = openpyxl.load_workbook("Beerco_kiosk_data.xlsx")
    dataframe1 = dataframe.active
    d = 0
    p = 5
    sp = 1
    sf = 1234
    for row in dataframe1.iter_rows(2, dataframe1.max_row):
        new_beer = Beer(id=d,price=p,name=str(row[2].value),brewer=str(row[3].value),region=str(row[4].value),
                        country=str(row[5].value),state=str(row[6].value),tempBeerStyle1=str(row[8].value),
                        tempBeerStyle2=str(row[9].value),primaryBeerStyle=str(row[10].value),primaryBeerStyleDesc=str(row[11].value),
                        specificBeerStyle=str(row[12].value),specificBeerStyleDesc=str(row[13].value),foodPairing=str(row[14].value),oz=str(row[15].value),
                        ml=str(row[16].value),container=str(row[17].value),abv=str(row[19].value),ibu=str(row[20].value),
                        srm=str(row[21].value),malt=str(row[22].value),hops=str(row[23].value),cals=str(row[25].value),
                        desc=str(row[26].value),special=sp,searchFreq=sf)
        db.session.add(new_beer)
        db.session.commit()
        if d >= 3:
            sp = 0
            p = float(random.randint(10, 15))
        sf = random.randint(0, 1000)
        d += 1
    print('DB initialized!')

def findTotal(cart):
    total = 0.0
    for item in cart:
        total += float(item.price)
    return total
