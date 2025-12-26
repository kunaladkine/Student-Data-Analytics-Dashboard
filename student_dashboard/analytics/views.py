from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.core.files.storage import FileSystemStorage
# Create your views here.


uploaded_df=None

def dashboard(request):
    return render(request, "analytics/dashboard.html")

def upload_data(request):
    global uploaded_df
    context = {}

    if request.method == "POST":
        file = request.FILES.get('csv_file')

        if not file:
            context["error"] = "Please upload a CSV file"
            return render(request, "analytics/upload.html", context)

        try:
            df = pd.read_csv(file)  # ⬅ DIRECTLY READ FILE (BEST METHOD)
            uploaded_df = df
            context["df"] = df.to_html(classes="table table-bordered table-striped")

        except Exception as e:
            context["error"] = f"Error reading file: {e}"

    return render(request, "analytics/upload.html", context)

def statistics_view(request):
    global uploaded_df
    if uploaded_df is None:
        return render(request,"analytics/statistics.html",{"error":"please upload a file first"})
    marks =np.array(uploaded_df.iloc[:,1])

    context={
        "average":np.mean(marks),
        "highest":np.max(marks),
        "lowest":np.min(marks),
        "std_dev":np.std(marks),
    }

    return render(request, "analytics/statistics.html",context)

def chart_view(request):
    global uploaded_df
    if uploaded_df is None:
        return render(request,"analytics/statistics.html",{"error":"upload Data First"})
    
    plt.figure(figsize=(6,4))
    plt.bar(uploaded_df.iloc[:,0],uploaded_df.iloc[:,1])
    plt.xlabel("stuents")
    plt.ylabel("Marks")
    plt.title("Student Performance Chart")

    buffer=BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic=base64.b64encode(buffer.getvalue()).decode('utf-8')

    buffer.close()

    return render(request, "analytics/chart.html",{"chart":graphic})
