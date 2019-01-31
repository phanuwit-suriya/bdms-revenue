import sys
from decimal import getcontext

import olap.xmla.xmla as xmla
from flask import Flask, json, render_template

app = Flask(__name__)


def data_cube(statement, catalog):
    provider = xmla.XMLAProvider()
    connect = provider.connect(
        location='http://10.88.10.163/OLAP/msmdpump.dll',
        username='cacheconnect',
        password='connect'
    )
    # source = connect.getOLAPSource()

    resource = connect.Execute(statement, Catalog=catalog)
    getSlice = resource.getSlice(properties='Value')
    getAxisTuple = resource.getAxisTuple(1)

    if len(getSlice) == len(getAxisTuple):
        data = []
        for val1, val2 in iter(zip(getAxisTuple, getSlice)):
            data.append([val1['Caption'], val2[0]])
        return data
    else:
        return


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/revenue')
def revenue():
    with open('./thailand-geojson/thailand-provinces-geojson.json') as f:
        geojson = json.load(f)
        statement1 = """
        select
        non empty {[Measures].[Net Amt]} on columns,
        non empty {[Patient Address].[Region - Province - City].[Province Desc].members} on rows
        from [BHQ Medtrack Revenue by Processing Marketing]
        """
        statement2 = """
        select
        non empty {[Measures].[Discount Amt]} on columns,
        non empty {[Patient Address].[Region - Province - City].[Province Desc].members} on rows
        from [BHQ Medtrack Revenue by Processing Marketing]
        """
        statement3 = """
        select
        non empty {[Measures].[Episode Number]} on columns,
        non empty {[Patient Address].[Region - Province - City].[Province Desc].members} on rows
        from [BHQ Medtrack Revenue by Processing Marketing]
        """
        catalog = "BHQ Medtrack Revenue by Processing Marketing"

        return render_template(
            'revenue.html',
            netamount=json.dumps(data_cube(statement1, catalog)),
            discountamount=json.dumps(data_cube(statement2, catalog)),
            episodenumber=json.dumps(data_cube(statement3, catalog)),
            geojson=json.dumps(geojson)
        )

@app.route('/thailand')
def thailand():
    with open('./thailand-geojson/thailand-provinces-geojson.json') as f:
        geojson = json.load(f)
        statement1 = """
        select
        non empty {[Measures].[Net Amt]} on columns,
        non empty {[Patient Address].[Region - Province - City].[Province Desc].members} on rows
        from [BHQ Medtrack Revenue by Processing Marketing]
        """
        catalog = "BHQ Medtrack Revenue by Processing Marketing"

        return render_template(
            'thailand.html',
            netamount=json.dumps(data_cube(statement1, catalog)),
            geojson=json.dumps(geojson)
        )


if __name__ == '__main__':
    app.run(debug=True)
