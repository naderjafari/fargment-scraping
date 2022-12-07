
from ton_api import get_all_auctions
from models import Auction
from config import app, db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, not_
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app.app_context().push()


def add_auction(auction):
    try:
        db.session.add(auction)
        db.session.commit()
    except IntegrityError:
        print(auction, "Already exist")
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def get_auction(domain, date):
    return db.session.query(Auction).filter(and_(
        Auction.domain == domain, Auction.date == date
    )
    ).first()


def update_auction(auction):
    print('Update ', auction)
    try:
        db.session.commit()
    except:
        print("Roll Back")
        db.session.rollback()
        raise
    finally:
        # print("Close the connection.")
        db.session.close()  # optional, depends on use case


def add_auctions():
    with app.app_context():
        tonapi_auctions = get_all_auctions()
        print('We get ', len(tonapi_auctions), 'Number of auctions')

        for item in tonapi_auctions:
            date = int(item['date'])
            price = int(item['price'])
            action = get_auction(item['domain'], date)
            if action == None:
                add_auction(Auction(
                    domain=item['domain'], date=date, price=price))
            else:
                if action.price != price:
                    action.price = price
                    update_auction(action)


# with app.app_context():
scheduler = BackgroundScheduler()
scheduler.add_job(func=add_auctions, trigger="interval", seconds=5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def nader():
    return "Hi"


# @app.route('/insert')


@app.route('/test')
def test():

    auction = get_auction('portapp.t.me', '1670417000')

    print(auction)

    return 'OK'


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
