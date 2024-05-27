from django.shortcuts import render, redirect
from .forms import SearchForm
import csv
import os 
import pandas as pd 
# from .models import JinaBase
from django.http import JsonResponse
import json
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import numpy as np
import io
from io import BytesIO
import base64
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import JinabaseSerializer
from .models import JinaBase
from rest_framework.response import Response
from rest_framework.decorators import action
# Django administration
# username: roaa
# password: jvao.123456789

class JinabaseViewSet(viewsets.ModelViewSet):
    queryset = JinaBase.objects.all()
    serializer_class = JinabaseSerializer

    @action(detail=False, methods=['post'])
    def plot_data(self, request):
        x_column = request.data.get('xColumn')
        y_column = request.data.get('yColumn')

        if x_column and y_column:
            csv_file_path = "jinaapp/static/jinaapp/JINAbase2021_RA_DEC_deg.csv"
            df = pd.read_csv(csv_file_path)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.set_facecolor("#F5F5F5")

            plt.xlabel(x_column, fontsize=20, color='#64467C', fontweight='bold')
            plt.ylabel(y_column, fontsize=20, color='#64467C', fontweight='bold')

            plot_dynamic_condition(ax, df, x_column, y_column, condition_x='<', condition_y='<', marker='o', color='orange')
            
            # Get the graph as base64 encoded string
            graph = get_graph(fig)
            plt.close(fig)

            return Response({'graph': graph})
        else:
            return Response({'error': 'Please select both X and Y columns.'}, status=400)



    @action(detail=False, methods=['post'])
    def show_table(self, request):
        x_column = request.data.get('xColumn')
        y_column = request.data.get('yColumn')

        if x_column and y_column:
            csv_file_path = "jinaapp/static/jinaapp/JINAbase2021_RA_DEC_deg.csv"
            df = pd.read_csv(csv_file_path)

            # Remove "<" sign from columns and replace empty strings with NaN
            df[x_column] = df[x_column].str[1:].replace('', np.nan).astype(float)
            df[y_column] = df[y_column].str[1:].replace('', np.nan).astype(float)

            # Filter rows with missing values after conversion
            df.dropna(subset=[x_column, y_column], inplace=True)

            # Filter data based on x and y columns
            filtered_df = df[(df[x_column] < 10) & (df[y_column] < 20)]  # Example filtering condition

            # Convert filtered DataFrame to list of dictionaries
            table_data = filtered_df.to_dict(orient='records')

            # Replace out-of-range float values with a placeholder
            for record in table_data:
                for key, value in record.items():
                    if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                        record[key] = 'NaN'  # Placeholder value for out-of-range float values

            return Response({'table_data': table_data})
        else:
            return Response({'error': 'Please select both X and Y columns.'}, status=400)








        

def index(request):
    return render(request, 'jinaapp/index.html')



def get_csv_columns(csv_file_path):
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        columns = next(reader)
    return columns


def filter_csv(column_name, value, csv_file_path):
    filtered_data = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if column_name in row and row[column_name] == value:
                filtered_data.append(row)
    return filtered_data

columns = ['Li', 'Be', 'C', 'N', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'Sn', 'Te', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'W', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Pb', 'Bi', 'Th', 'U', 'TiII', 'VII', 'MnII', 'FeII']

def get_data(request):
    all_data = get_all_data()

    return JsonResponse(all_data, safe=False)

def get_unique_val(column):
    csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/jinaapp/JINAbase2021_RA_DEC_deg.csv')
    data = pd.read_csv(csv_file_path)
    return data[column].unique()

def filter_data(request):
    filtered_data = []
    if request.method == 'POST':
        # teffrom = request.POST.get('TeffFrom')
        # teffto = request.POST.get('TeffTo')
        # loggfrom = request.POST.get('loggFrom')
        # loggto = request.POST.get('loggTo')
        # feHfrom = request.POST.get('Fe_HFrom')
        # feHto = request.POST.get('Fe_HTo')
        
        teff = request.POST.get('Teff')
        logg = request.POST.get('logg')
        feH = request.POST.get('fe_H')

        refValue = request.POST.get('Ref')
        el1 = request.POST.get('el1')
        from1 = request.POST.get('from1')
        to1 = request.POST.get('to1')
        el2 = request.POST.get('el2')
        from2 = request.POST.get('from2')
        to2 = request.POST.get('to2')
        el3 = request.POST.get('el3')
        from3 = request.POST.get('from3')
        to3 = request.POST.get('to3')



        filters = {}

        if refValue:
            filters['Ref'] = refValue
        
        

        if teff:
            filters['Teff'] = teff

        if logg:
            filters['logg'] = logg

        if feH:
            filters['Fe_H'] = feH

        # if el1 and from1 is not None and to1 is not None:
        #     filters[el1] = from1
        #     filters[el1] = to1
        #     filters[el1 + '__gte'] = from1
        #     filters[el1 + '__lte'] = to1
            
        # if el2 and from2 is not None and to2 is not None:
        #     filters[el2] = from2
        #     filters[el2] = to2
        #     filters[el1 + '__gte'] = from1
        #     filters[el1 + '__lte'] = to1
            
        # if el1 and from3 is not None and to3 is not None:
        #     filters[el3] = from3
        #     filters[el3] = to3
        #     filters[el1 + '__gte'] = from1
        #     filters[el1 + '__lte'] = to1
            
        
           
        if not filters:
            return JsonResponse({'error': 'Filter parameters are missing'}, status=400)

        all_data = get_all_data()


        
        filtered_data = [record for record in all_data if all(key in record and str(record[key]) == value for key, value in filters.items())]

    elements_list = ["Li", "Be", "C", "N", "O", "F", "Na", "Mg", "Al", "Si", "P", "S", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Ru", "Rh", "Pd", "Ag", "Cd", "Sn", "Te", "Ba", "La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "W", "Os", "Ir", "Pt", "Au", "Hg", "Pb", "Bi", "Th", "U"]

    context = {
        'filtered_data': filtered_data,
        'available_fields': ['Teff', 'Ref', 'logg', 'Fe_H'] + elements_list,  
        'selected_fields': ['Teff', 'Ref', 'logg', 'Fe_H'] + elements_list,  
        'unique_refs': get_unique_val('Ref'),
        'unique_el': elements_list,
        'columns': columns,
    }

    return render(request, 'jinaapp/query.html', context)

def get_all_data():
    json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/jinaapp/JINAbase2021_RA_DEC_deg.json')

    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)

        return json_data
    else:
        return []

def get_graph(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph

def plot_data(request):
    if request.method == 'POST' and request.is_ajax():
        x_column = request.POST.get('xColumn')
        y_column = request.POST.get('yColumn')

        if x_column and y_column:
            csv_file_path = "jinaapp/static/jinaapp/JINAbase2021_RA_DEC_deg.csv"
            df = pd.read_csv(csv_file_path)

            fig, ax = plt.subplots()
            plt.switch_backend('AGG')
            plt.figure(figsize=(10, 5))
            plot_dynamic_condition(ax, df, x_column, y_column, condition_x='<', condition_y='<', marker='o', color='orange')
            
            # Get the graph as base64 encoded string
            graph = get_graph(fig)
            plt.close(fig)

            response_data = {
                'graph': graph
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Please select both X and Y columns.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

def plot_dynamic_condition(ax, df, x_column, y_column, condition_x='', condition_y='', marker='o', color='orange'):
    if condition_x:
        df = df[df[x_column].str[0] == condition_x]
    if condition_y:
        df = df[df[y_column].str[0] == condition_y]

    df = df.reset_index()

    x = np.asarray(df[x_column].str[1:], dtype=float) if condition_x else np.asarray(df[x_column], dtype=float)
    y = np.asarray(df[y_column].str[1:], dtype=float) if condition_y else np.asarray(df[y_column], dtype=float)

    if condition_x or condition_y:
        ax.errorbar(x, y + x, 0.3, 0.3, marker=marker, c=color, mfc='white', ms=10, capsize=5, lw=3, uplims=True,
                    xuplims=True, ls='none')
    else:
        ax.plot(x, y + x, marker, color=color, markerfacecolor='white', linewidth=3, markersize=10, zorder=0)


# def convert_csv_to_json(csv_filename, json_filename):
#     df = pd.read_csv(csv_filename)

#     df['id'] = range(1, len(df) + 1)

#     json_data = df.to_json(orient='records')

#     parsed_json_data = json.loads(json_data)

#     with open(json_filename, 'w') as json_file:
#         json.dump(parsed_json_data, json_file, indent=4)

# csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/jinaapp/JINAbase2021_RA_DEC_deg.csv')
# json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/jinaapp/JINAbase2021_RA_DEC_deg.json')

# convert_csv_to_json(csv_file_path, json_file_path)
        

