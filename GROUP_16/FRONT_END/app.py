from flask import Flask, render_template, session, url_for, session, request, jsonify, make_response, redirect
import json
import psycopg2
import datetime

try:
    con = psycopg2.connect(dbname='dbms_project',user='postgres',host='localhost',password='2311Weep')
    # con = psycopg2.connect(dbname='temp',user='postgres',host='localhost',password='mayur')

    print("Connected....")
except:
    print("Cannot connect to database....")
    exit(0)
cur = con.cursor()

app = Flask(__name__)

app.secret_key = b'lol'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search_home():
    return render_template('search_home.html')

@app.route('/search_year',methods=["GET","POST"])
def search_year():
    if request.method == 'POST':
        print("Hello")

    cur.execute("select state_name from state")
    con.commit()
    state_data = cur.fetchall()

    district_data = []

    cur.execute("select distinct commodity_name from commodity;")
    con.commit()
    commodity_data = cur.fetchall()

    commodity_data_variety = []

    return render_template('search_year.html',state_data = state_data,district_data=district_data,commodity_data=commodity_data,
        commodity_data_variety=commodity_data_variety)

@app.route('/search_record',methods=["GET","POST"])
def search_record():
    if request.method == 'POST':
        print("Hello")
    con.commit()
    cur.execute("select state_id,state_name from state")
    state_data = cur.fetchall()

    con.commit()
    cur.execute("select district_id,district_name from district")
    district_data = cur.fetchall()

    con.commit()
    cur.execute("select market_id,market_name from market;")
    market_data = cur.fetchall()


    return render_template('search_record.html',state_data = state_data,district_data=district_data,market_data=market_data)

@app.route('/search_location',methods=["GET","POST"])
def search_location():
    if request.method == 'POST':
        print("Hello")

    con.commit()
    cur.execute("select state_name from state")
    state_data = cur.fetchall()

    con.commit()
    cur.execute("select district_name from district")
    district_data = cur.fetchall()

    con.commit()
    cur.execute("select distinct extract(year from arrival_date)::int as year from daily_prices order by year")
    year_data = cur.fetchall()

    con.commit()
    cur.execute("select distinct commodity_name from commodity;")
    commodity_data = cur.fetchall()

    return render_template('search_location.html',state_data = state_data,district_data=district_data,year_data=year_data,commodity_data=commodity_data)


@app.route('/search_results',methods=["GET","POST"])
def search_results():
    data = []
    if request.method == 'POST':
        state = str(request.form['state'])
        district_id = str(request.form['district'])
        commodity = str(request.form['commodity'])
        print(state,district_id,commodity)
        sql = "select d.year::int , round(max(d.max_price)::numeric,2)::int, round(min(d.min_price)::numeric,2)::int , round(avg(d.modal_price)::numeric,2)::int        \
                    from (select * from state where state_name = %s) st                                                                              \
                    inner join (select * from district where district_id = %s)  dt on dt.state_id = st.state_id                                        \
                    inner join market m on m.district_id = dt.district_id                                                                                               \
                    inner join (select record_id, market_id, variety_id,extract (year from arrival_date) as year, min_price, max_price,modal_price from daily_prices  \
                        where  min_price > 0 and max_price > 0 and modal_price > 0) d                                                                                   \
                        on d.market_id = m.market_id                                                                                                                    \
                    inner join variety v on v.variety_id = d.variety_id  \
                    inner join (select * from commodity where commodity_name = %s) c on c.commodity_id = v.commodity_id                                           \
                    group by d.year                                                                                                                                     \
                    order by d.year;"
        con.commit()
        cur.execute(sql,(state,district_id,commodity))
        data = cur.fetchall()
        print(data)

    return render_template('search_results.html',data=data)

@app.route('/search_results_record',methods=["GET","POST"])
def search_results_record():
    data = []
    state = None
    district_name = [None]
    market_name = [None]
    if request.method == 'POST':
        state = str(request.form['state'])
        district = str(request.form['district'])
        sql = "select district_name from district where district_id=%s"
        con.commit()
        cur.execute(sql,(district,))
        district_name = cur.fetchall()
        market = str(request.form['market'])
        sql = "select market_name from market where market_id=%s"
        con.commit()
        cur.execute(sql,(market,))
        market_name = cur.fetchall()

        print(market_name)
        sql = "select commodity.commodity_name, variety.variety_name, daily_prices.arrival_date, daily_prices.max_price::int, daily_prices.min_price::int, daily_prices.modal_price::int \
                from daily_prices \
                inner join market on market.market_id = daily_prices.market_id and market.market_id = %s \
                inner join variety on variety.variety_id = daily_prices.variety_id \
                inner join commodity on commodity.commodity_id = variety.commodity_id \
                order by daily_prices.arrival_date desc \
                limit 100" 
        con.commit()
        cur.execute(sql,(market,))
        data = cur.fetchall()
        print(data)

    return render_template('search_results_record.html',data=data,state=state,district=district_name[0],market=market_name[0])

@app.route('/search_results_year',methods=["GET","POST"])
def search_results_year():
    data = []
    district_name = [None]
    state = None
    district = None
    commodity = None
    variety = None

    if request.method == 'POST':
        state = str(request.form['state'])
        district = str(request.form['district'])
        commodity = str(request.form['commodity'])
        sql = "select district_name from district where district_id=%s"
        con.commit()
        cur.execute(sql,(district,))
        district_name = cur.fetchall()


        variety = str(request.form['variety'])
        print(state,district,district_name,commodity,variety)
        print(variety)
        if variety == "All":
            print("Hello")
            sql = "with d as (\
                    select record_id, market_id, daily_prices.variety_id,extract (year from arrival_date) as year, min_price, max_price,modal_price\
                    from daily_prices\
                    inner join variety v on v.variety_id = daily_prices.variety_id  \
                    inner join commodity on commodity.commodity_id = v.commodity_id and commodity.commodity_name = %s\
                    where market_id in (select market.market_id from market\
                                        where market.district_id = %s)\
                     and min_price > 0 and max_price > 0 and modal_price > 0\
                )\
                select d.year::int , round(max(d.max_price)::numeric,2)::int, round(min(d.min_price)::numeric,2)::int , round(avg(d.modal_price)::numeric,2)::int\
                from d\
                group by d.year\
                order by d.year;"
            con.commit()
            cur.execute(sql,(commodity,district))
            data = cur.fetchall()
        else:
            sql = "with d as (\
                    select record_id, market_id, daily_prices.variety_id,extract (year from arrival_date) as year, min_price, max_price,modal_price\
                    from daily_prices\
                    inner join variety v on v.variety_id = daily_prices.variety_id  and v.variety_name = %s \
                    inner join commodity on commodity.commodity_id = v.commodity_id and commodity.commodity_name = %s\
                    where market_id in (select market.market_id from market\
                                        where market.district_id = %s)\
                     and min_price > 0 and max_price > 0 and modal_price > 0\
                )\
                select d.year::int , round(max(d.max_price)::numeric,2)::int, round(min(d.min_price)::numeric,2)::int , round(avg(d.modal_price)::numeric,2)::int\
                from d\
                group by d.year\
                order by d.year;"
            con.commit()
            cur.execute(sql,(variety,commodity,district))
            data = cur.fetchall()

    return render_template('search_results.html',data=data,district=district_name[0],state=state,commodity=commodity,variety=variety)

temp_data = {'commodity':None,'state':None}
@app.route('/search_results_location',methods=["GET","POST"])
def search_results_location():
    data = []
    con.commit()
    cur.execute("select state_name from state")
    state_data = cur.fetchall()
    if request.method == 'POST':
        try:
            commodity = str(request.form['commodity'])
            temp_data['commodity'] = commodity
            temp_data['state'] = None
        except Exception as e:
            commodity = temp_data['commodity']

        try:
            state = str(request.form['state'])
            temp_data['state'] = state
        except Exception as e:
            state = temp_data['state']

        print(commodity,state)

        if state==None:
            sql = "select st.state_name, dt.district_name, d.year::int, round(max(d.max_price)::numeric,2)::int, round(min(d.min_price)::numeric,2)::int , round(avg(d.modal_price)::numeric,2)::int \
            from state st \
            inner join district dt on dt.state_id = st.state_id \
            inner join market m on m.district_id = dt.district_id \
            inner join (select record_id, market_id, variety_id,extract (year from arrival_date) as year, min_price, max_price,modal_price from daily_prices \
                where  min_price > 0 and max_price > 0 and modal_price > 0) d \
                on d.market_id = m.market_id \
            inner join variety v on v.variety_id = d.variety_id  \
            inner join (select * from commodity where commodity_name = %s) c on c.commodity_id = v.commodity_id \
            group by st.state_name, dt.district_name, d.year \
            order by st.state_name, dt.district_name, d.year;"

            con.commit()
            cur.execute(sql,(commodity,))
        else:
            sql = "select st.state_name, dt.district_name, d.year::int, round(max(d.max_price)::numeric,2)::int, round(min(d.min_price)::numeric,2)::int , round(avg(d.modal_price)::numeric,2)::int \
            from state st \
            inner join district dt on dt.state_id = st.state_id \
            inner join market m on m.district_id = dt.district_id \
            inner join (select record_id, market_id, variety_id,extract (year from arrival_date) as year, min_price, max_price,modal_price from daily_prices \
                where  min_price > 0 and max_price > 0 and modal_price > 0) d \
                on d.market_id = m.market_id \
            inner join variety v on v.variety_id = d.variety_id  \
            inner join (select * from commodity where commodity_name = %s) c on c.commodity_id = v.commodity_id \
            where st.state_name = %s \
            group by st.state_name, dt.district_name, d.year \
            order by st.state_name, dt.district_name, d.year;"
            con.commit()
            cur.execute(sql,(commodity,state))
            # print(cur.query)
        data = cur.fetchall()

    return render_template('search_results_location.html',data=data,state_data=state_data)  


@app.route('/market',methods=['GET', 'POST'])
def market():
    if request.method == 'POST':
        print("Hello")

    con.commit()
    cur.execute("select state_name from state")
    state_data = cur.fetchall()

    district_data = []

    con.commit()
    cur.execute("select distinct commodity_name from commodity;")
    commodity_data = cur.fetchall()

    commodity_data_variety = []

    return render_template('market.html',state_data = state_data,district_data=district_data,commodity_data=commodity_data,
        commodity_data_variety=commodity_data_variety)

@app.route('/market_result',methods=['GET', 'POST'])
def market_result():
    if request.method != 'POST':
        print("Hello")
        return redirect(url_for('market'))
    state = str(request.form['state'])
    district = request.form['district']
    commodity = str(request.form['commodity'])
    variety = str(request.form['variety'])
    month = int(request.form['month'])
    print(state)
    print(district)
    print(commodity)
    print(variety)
    print(month)
    print(variety)
    if variety.lower() !='all':
        sql = """with net_prices as (
            select dis.d2_id as district_id, round(avg(pt.modal_price_avg) - 0.6*avg(dis.dist))::int as net_price, avg(dis.dist)::int as dist
            from (select * from district where district_id = %s) d 
            inner join state s on d.state_id = s.state_id and s.state_name = %s
            inner join distances dis on dis.d1_id = d.district_id and dis.dist < 500
            inner join market m on dis.d2_id = m.district_id
            inner join price_trend pt on m.market_id = pt.market_id and pt.variety_id in (select variety_id from commodity,variety where commodity.commodity_id = variety.commodity_id and commodity_name = %s and variety_name = %s)and pt.month = %s
            group by dis.d2_id
            )
            select np.*, d.district_name, s.state_name
            from (select * from net_prices order by net_price desc limit 10) np
            inner join district d on d.district_id = np.district_id
            inner join state s on d.state_id = s.state_id
            order by np.net_price desc;"""

        con.commit()
        cur.execute(sql,(district,state,commodity,variety,month))
        data = cur.fetchall()
    else:
        sql = """with net_prices as (
            select dis.d2_id as district_id, round(avg(pt.modal_price_avg) - 0.6*avg(dis.dist))::int as net_price, avg(dis.dist)::int as dist
            from (select * from district where district_id = %s) d 
            inner join state s on d.state_id = s.state_id and s.state_name = %s
            inner join distances dis on dis.d1_id = d.district_id and dis.dist < 500
            inner join market m on dis.d2_id = m.district_id
            inner join price_trend pt on m.market_id = pt.market_id and pt.variety_id in (select variety_id from commodity,variety where commodity.commodity_id = variety.commodity_id and commodity_name = %s)and pt.month = %s
            group by dis.d2_id
            )
            select np.*, d.district_name, s.state_name
            from (select * from net_prices order by net_price desc limit 10) np
            inner join district d on d.district_id = np.district_id
            inner join state s on d.state_id = s.state_id
            order by np.net_price desc;"""

        con.commit()
        cur.execute(sql,(district,state,commodity,month))
        data = cur.fetchall()
    print(data)
    return render_template('recommendation_result.html',data=data)


@app.route('/getDistricts',methods=["GET"])
def get_distrcits():
    
    state_name = request.args.get('state_name',None)

    if state_name == None:
        con.commit()
        cur.execute("SELECT * from district;")
        district_data = cur.fetchall()
    else:
        sql = "select district.district_id, district.district_name \
            from district \
            inner join state on district.state_id = state.state_id\
            where state.state_name = %s;"
        con.commit()
        cur.execute(sql,(state_name,))
        district_data = cur.fetchall()

    return jsonify(district_data)

@app.route('/getVariety',methods=["GET"])
def get_varieties():
    
    commodity_name = request.args.get('commodity_name',None)

    if commodity_name == None:
        variety_data = []
    else:
        sql = "select commodity.commodity_id, commodity.variety \
            from commodity \
            where commodity.commodity_name = %s;"

        sql = """ select variety_id,variety_name from variety where commodity_id in (select commodity_id from commodity where commodity_name = %s)"""
        con.commit()
        cur.execute(sql,(commodity_name,))
        variety_data = cur.fetchall()

    return jsonify(variety_data)

@app.route('/getMarkets',methods=["GET"])
def get_markets():
    
    district_id = request.args.get('district_name',None)
    state_name = request.args.get('state_name',None)

    if state_name == None:
        con.commit()
        cur.execute("SELECT * from market;")
        market_data = cur.fetchall()
    elif district_id == None:
        sql = "select market.market_id, market.market_name from market\
                inner join district on market.district_id = district.district_id\
                inner join state on state.state_id = district.state_id\
                where state_name = '" + state_name + "';"
        con.commit()
        cur.execute(sql)
        market_data = cur.fetchall()
    else:
        sql = "select market.market_id, market.market_name from market\
                inner join district on market.district_id = district.district_id and district.district_id = '" + district_id + "'\
                inner join state on state.state_id = district.state_id\
                where state_name = '" + state_name + "';"
        con.commit()
        cur.execute(sql)
        market_data = cur.fetchall()

    return jsonify(market_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add',methods=["GET"])
def add_price_data():
    con.commit()
    cur.execute("select state_name from state")
    state_data = cur.fetchall()

    district_data = []

    con.commit()
    cur.execute("select distinct commodity_name from commodity;")
    commodity_data = cur.fetchall()

    commodity_data_variety = []

    market_data = []
    return render_template('add.html',state_data = state_data,district_data=district_data,commodity_data=commodity_data,
        commodity_data_variety=commodity_data_variety,market_data=market_data)

@app.route('/insert',methods=["POST"])
def insert_data():

    variety = str(request.form['variety'])
    market = request.form['market']
    arrival_date = datetime.datetime.strptime(request.form['arrival_date'],"%Y-%m-%d")
    price = request.form['price']
    comment = request.form.get('comment'," ")
    print(market)
    print(price)
    print(variety)
    print(comment)
    # '""" + arrival_date.strftime("%d-%m-%Y") + """',
    sql = """insert into transaction_prices(market_id,transaction_date,price,variety_id,comment) values
            (%s,
            %s,
            %s,
            %s,
            %s
            );
            """
    cur.execute(sql,(market,arrival_date.strftime("%d-%m-%Y"),price,variety,comment))
    con.commit()
    return render_template('add_success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('add')
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug = False)
