# 00 FullName  
# 01 WineryName  
# 02 AppellationLevel  
# 03 AppellationName  
# 04 Region  
# 05 Pairing  
# 06 RS  
# 07 QP  
# 08 Rank  
# 09 Price  
# 10 EvaluationAvg  
# 11 WineType  
# 12 Grapes  
# 13 AgingMonths  
# 14 AgingType  
# 15 RS2  
# 16 QP2  
# 17 RS3  
# 18 QP3  
# 19 RANK2  
# 20 RANK3  
# 21 RatingYear  
# 22 Vintage  
# 23 ScoreAvg  
# 24 Tasting  
# 25 SLC  
# 26 TLC
# 27 QPRANK


from flask import Flask, request, render_template
import json
import statistics
import sqlite3

app = Flask(__name__)

def load_data():
   with open('static/pages/home.json') as f:
      data = json.load(f)
   return data

@app.route("/")
def home():
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM allwines WHERE Entry = 1')    
    count = c.fetchone()[0]
    conn.close()

    data = load_data()

    data['body'] = data['body'].replace('{count}', str(count))

    return render_template('home.html.j2', **data)

@app.route("/documentation")
def documentation():

    return render_template('documentation.html.j2',)


@app.route("/search", methods=['GET', 'POST'])
def show_entries():
    if request.method == 'POST':
        search_query = request.form['q']
        conn = sqlite3.connect('allwines.db')
        c = conn.cursor()
        if len(search_query.split()) > 1:
            wildcard_query = '%' + '%'.join(search_query.split()) + '%'
            c.execute(
                'SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS, QP, Rank, Price, EvaluationAvg, WineType, Grapes, AgingMonths, AgingType, RS2, QP2, RS3, QP3, RANK2, RANK3, RatingYear, Vintage, ScoreAvg, Tasting, SLC, TLC, QPRANK FROM allwines WHERE Entry = 1 AND (FullName LIKE ? OR WineryName LIKE ? OR Pairing LIKE ? OR FullName LIKE ? OR FullName LIKE ? OR WineryName LIKE ? OR WineryName LIKE ? OR Pairing LIKE ? OR Pairing LIKE ?)',
                (wildcard_query, wildcard_query, wildcard_query, '%' + search_query.split()[0] + '% %' + search_query.split()[1] + '%', '%' + search_query.split()[1] + '% %' + search_query.split()[0] + '%', '%' + search_query.split()[0] + '% %' + search_query.split()[1] + '%', '%' + search_query.split()[1] + '% %' + search_query.split()[0] + '%', '%' + search_query.split()[0] + '% %' + search_query.split()[1] + '%', '%' + search_query.split()[1] + '% %' + search_query.split()[0] + '%')
            )
        else:
            c.execute(
                'SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS, QP, Rank, Price, EvaluationAvg, WineType, Grapes, AgingMonths, AgingType, RS2, QP2, RS3, QP3, RANK2, RANK3, RatingYear, Vintage, ScoreAvg, Tasting, SLC, TLC, QPRANK FROM allwines WHERE Entry = 1 AND (FullName LIKE ? OR WineryName LIKE ? OR Pairing LIKE ?)',
                ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%')
            )
        entries = c.fetchall()
        conn.close()

        appellation_counts = {}

        for entry in entries:
            appellation_name = entry[3]  # index 3 is the AppellationName column in the database

            # execute SQL query to get the count of entries with the same AppellationName
            conn = sqlite3.connect('allwines.db')
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM allwines WHERE Entry = 1 AND AppellationName = ?', (appellation_name,))
            count = c.fetchone()[0]  # fetchone returns a tuple, but we only want the count value (index 0)
            conn.close()

            appellation_counts[appellation_name] = count

        count = len(entries)

        return render_template('search.html.j2', search_query=search_query, count=count, entries=entries, appellation_counts=appellation_counts)
    else:
        return render_template('search.html.j2', search_query='', count=0, entries=[], appellation_counts={})
    
# @app.route("/allwines")
# def all_wines():
#     conn = sqlite3.connect('allwines.db')
#     c = conn.cursor()
#     c.execute('SELECT FullName, WineryName FROM allwines WHERE Entry = 1')
#     entries = c.fetchall()
#     conn.close()

#     count = len(entries)
#     return render_template('home.html.j2', entries=entries, count=count, search_query='')
    
@app.route("/wine")
def show_wine():
    fullname = request.args.get('fullname')
    wineryname = request.args.get('wineryname')

    # fetch data from the database using fullname and wineryname
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()
    
    c.execute('SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS, QP, Rank, Price, EvaluationAvg, WineType, Grapes, AgingMonths, AgingType, RS2, QP2, RS3, QP3, RANK2, RANK3, RatingYear, Vintage, ScoreAvg, Tasting, SLC, TLC, QPRANK FROM allwines WHERE FullName = ? AND WineryName = ? AND Entry = 1', (fullname, wineryname))
    wine_data = c.fetchone()

    appellation_name = wine_data[3] 
    wine_type = wine_data[11]
    wine_slc = wine_data[25]
    wine_tlc = wine_data[26] 

    #total wines with the same RS
    c.execute('SELECT COUNT(*) FROM allwines WHERE AppellationName = ? AND WineType = ? AND Entry = 1', (appellation_name, wine_type))
    wine_type_count = c.fetchone()[0]

    #total wines with the same RS2
    c.execute('SELECT COUNT(*) FROM allwines WHERE SLC = ? AND WineType = ? AND Entry = 1', (wine_slc, wine_type))
    wine_slc_count = c.fetchone()[0]

    #total wines with the same RS3
    c.execute('SELECT COUNT(*) FROM allwines WHERE TLC = ? AND WineType = ? AND Entry = 1', (wine_tlc, wine_type))
    wine_tlc_count = c.fetchone()[0]
    
    winery_name = wine_data[1]
    perc_rs_value= ((wine_data[6]-wine_data[8]+1)/wine_data[6]*100)
    perc_qp_value= ((wine_data[7]-wine_data[27]+1)/wine_data[7]*100)
    if wine_data[15] != '':
        perc_rs2_value= ((wine_data[15]-wine_data[19]+1)/wine_data[15]*100)
    else: 
        perc_rs2_value = 'null'
    if wine_data[17] != '':
        perc_rs3_value= ((wine_data[17]-wine_data[20]+1)/wine_data[17]*100)
    else: 
        perc_rs3_value = 'null'

    c.execute('SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS, QP, Rank, Price, EvaluationAvg, WineType, Grapes, AgingMonths, AgingType, RS2, QP2, RS3, QP3, RANK2, RANK3, RatingYear, Vintage, ScoreAvg, Tasting, SLC, TLC FROM allwines WHERE FullName = ? AND WineryName = ? AND Entry = 2', (fullname, wineryname))
    vintages_data = c.fetchall()

    c.execute('SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS, QP, Rank, Price, EvaluationAvg, WineType, Grapes, AgingMonths, AgingType, RS2, QP2, RS3, QP3, RANK2, RANK3, RatingYear, Vintage, ScoreAvg, Tasting, SLC, TLC FROM allwines WHERE AppellationName = ? AND Entry = 2', (wine_data[3],))
    appellation_data = c.fetchall()

    # Get minimum and maximum values of price
    prices = [row[9] for row in appellation_data]
    minmax = [min(prices), max(prices)]

    # Calculate median of appellation_data[i][9] by grouping by appellation_data[i][21]
    medians = []
    groups = {}
    for row in appellation_data:
        if row[21] in groups:
            groups[row[21]].append(row[9])
        else:
            groups[row[21]] = [row[9]]
            
    for key, val in groups.items():
        median_val = statistics.median(val)
        medians.append((key, median_val))

    # Sort medians by ascending order of key value
    medians = sorted(medians, key=lambda x: x[0])

    conn.close()

    return render_template('wine.html.j2', wine_data=wine_data, vintages_data=vintages_data, appellation_data=appellation_data, medians=medians, minmax=minmax, appellation_name=appellation_name, winery_name=winery_name, perc_rs_value=perc_rs_value, perc_qp_value=perc_qp_value, perc_rs2_value=perc_rs2_value, perc_rs3_value=perc_rs3_value, wine_type_count=wine_type_count, wine_slc_count=wine_slc_count, wine_tlc_count=wine_tlc_count)

@app.route("/winery/<winery_name>")
def show_winery(winery_name):
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()
    
    c.execute('SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS, QP, Rank, Price, EvaluationAvg, WineType, Grapes, AgingMonths, AgingType, RS2, QP2, RS3, QP3, RANK2, RANK3, RatingYear, Vintage, ScoreAvg, Tasting, SLC, TLC, QPRANK FROM allwines WHERE Entry = 1 AND WineryName = ?', (winery_name.replace("-", " "),))
    winery_wines = c.fetchall()
    
    wine_counts = []
    for wine in winery_wines:
        appellation_name = wine[3]
        wine_type = wine[11]
        c.execute('SELECT COUNT(*) FROM allwines WHERE Entry = 1 AND AppellationName = ? AND WineType = ?', (appellation_name, wine_type))
        count = c.fetchone()[0]
        wine_counts.append(count)

    conn.close()

    count = len(winery_wines)

    return render_template('winery.html.j2', winery_name=winery_name, count=count, winery_wines=winery_wines, wine_counts=wine_counts)

@app.route("/appellations/<appellation_name>")
def show_appellation(appellation_name):
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()

    c.execute('SELECT DISTINCT WineType FROM allwines WHERE Entry = 1 AND AppellationName = ?', (appellation_name.replace("-", " "),))
    wine_types = [row[0] for row in c.fetchall()]

    count_per_wine_type = {}
    for wine_type in wine_types:
        c.execute('SELECT COUNT(*) FROM allwines WHERE Entry = 1 AND AppellationName = ? AND WineType = ?', (appellation_name.replace("-", " "), wine_type))
        count_per_wine_type[wine_type] = c.fetchone()[0]

    c.execute('SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS, QP, Rank, Price, EvaluationAvg, WineType, Grapes, AgingMonths, AgingType, RS2, QP2, RS3, QP3, RANK2, RANK3, RatingYear, Vintage, ScoreAvg, Tasting, SLC, TLC, QPRANK FROM allwines WHERE Entry = 1 AND AppellationName = ?', (appellation_name.replace("-", " "),))
    entries = c.fetchall()
    conn.close()

    count = len(entries)

    return render_template('appellation.html.j2', appellation_name=appellation_name, count=count, entries=entries, wine_types=wine_types, count_per_wine_type=count_per_wine_type)

@app.route("/comparisons/<comparison>")
def show_comparison(comparison):
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()

    c.execute('SELECT DISTINCT WineType FROM allwines WHERE Entry = 1 AND AppellationName = ?', (comparison.replace("-", " "),))
    wine_types = [row[0] for row in c.fetchall()]

    count_per_wine_type = {}
    for wine_type in wine_types:
        c.execute('SELECT COUNT(*) FROM allwines WHERE Entry = 1 AND AppellationName = ? AND WineType = ?', (comparison.replace("-", " "), wine_type))
        count_per_wine_type[wine_type] = c.fetchone()[0]

    c.execute('SELECT FullName, WineryName FROM allwines WHERE Entry = 1 AND SLC = ?', (comparison,))
    wine_types = [row[0] for row in c.fetchall()]
    c.execute('SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS, QP, Rank, Price, EvaluationAvg, WineType, Grapes, AgingMonths, AgingType, RS2, QP2, RS3, QP3, RANK2, RANK3, RatingYear, Vintage, ScoreAvg, Tasting, SLC, TLC, QPRANK FROM allwines WHERE Entry = 1 AND SLC = ?', (comparison.replace("-", " "),))
    entries = c.fetchall()
    conn.close()

    count = len(entries)

    return render_template('appellation.html.j2', comparison=comparison, count=count, entries=entries, wine_types=wine_types, count_per_wine_type=count_per_wine_type)

@app.route("/regional/<regional>")
def show_regional(regional):
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()

    c.execute('SELECT DISTINCT WineType FROM allwines WHERE Entry = 1 AND AppellationName = ?', (regional.replace("-", " "),))
    wine_types = [row[0] for row in c.fetchall()]

    count_per_wine_type = {}
    for wine_type in wine_types:
        c.execute('SELECT COUNT(*) FROM allwines WHERE Entry = 1 AND AppellationName = ? AND WineType = ?', (regional.replace("-", " "), wine_type))
        count_per_wine_type[wine_type] = c.fetchone()[0]

    c.execute('SELECT FullName, WineryName FROM allwines WHERE Entry = 1 AND TLC = ?', (regional,))
    wine_types = [row[0] for row in c.fetchall()]
    c.execute('SELECT FullName, WineryName, AppellationLevel, AppellationName, Region, Pairing, RS3, QP3, Rank, Price, EvaluationAvg, WineType FROM allwines WHERE Entry = 1 AND TLC = ?', (regional.replace("-", " "),))
    entries = c.fetchall()
    conn.close()

    count = len(entries)

    return render_template('appellation.html.j2', regional=regional, count=count, entries=entries, wine_types=wine_types, count_per_wine_type=count_per_wine_type)

@app.route("/docg_appellations")
def docg_appellations():
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT AppellationName, Region FROM allwines WHERE AppellationLevel = "DOCG" ORDER BY AppellationName ASC')
    appellations = c.fetchall()

    c.execute('SELECT AppellationName, COUNT(*) FROM allwines WHERE Entry = 1 AND AppellationLevel = "DOCG" GROUP BY AppellationName')
    appellations_with_counts = c.fetchall()
    counts = [count for _, count in appellations_with_counts]

    conn.close()

    count = len(appellations)

    return render_template('comparisons.html.j2', appellations=appellations, count=count, counts=counts)

@app.route("/doc_appellations")
def doc_appellations():
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT AppellationName, Region FROM allwines WHERE AppellationLevel = "DOC" ORDER BY AppellationName ASC')
    appellations = c.fetchall()

    c.execute('SELECT AppellationName, COUNT(*) FROM allwines WHERE Entry = 1 AND AppellationLevel = "DOC" GROUP BY AppellationName')
    appellations_with_counts = c.fetchall()
    counts = [count for _, count in appellations_with_counts]

    conn.close()

    count = len(appellations)

    return render_template('comparisons.html.j2', appellations=appellations, count=count, counts=counts)

@app.route("/slc")
def slc():
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT SLC, Region FROM allwines WHERE Entry = "1" AND SLC <> "" ORDER BY SLC ASC')
    appellations = c.fetchall()

    c.execute('SELECT SLC, COUNT(*) FROM allwines WHERE Entry = 1 AND SLC <> "" GROUP BY SLC')
    slc_with_counts = c.fetchall()
    counts = [count for _, count in slc_with_counts]
    conn.close()

    count = len(appellations)
    return render_template('comparisons.html.j2', appellations=appellations, count=count, counts=counts)

@app.route("/tlc")
def tlc():
    conn = sqlite3.connect('allwines.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT TLC, Region FROM allwines WHERE Entry = "1" AND TLC <> "" ORDER BY TLC ASC')
    appellations = c.fetchall()

    c.execute('SELECT TLC, COUNT(*) FROM allwines WHERE Entry = 1 AND TLC <> "" GROUP BY TLC')
    tlc_with_counts = c.fetchall()
    counts = [count for _, count in tlc_with_counts]
    conn.close()

    count = len(appellations)
    return render_template('comparisons.html.j2', appellations=appellations, count=count, counts=counts)

if __name__ == "__main__":
    app.run()