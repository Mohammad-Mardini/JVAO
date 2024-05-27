from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
from django.http import JsonResponse
import numpy as np
import pandas as pd 


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
