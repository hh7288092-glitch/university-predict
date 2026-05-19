from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# كود الواجهة الأكاديمية الزرقاء المنسقة بأيقونات الاقتصاد والإحصاء
html_layout = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة اختر تخصصك الجامعي بذكاء</title>
    <style>
        :root {
            --primary-blue: #1e3799;
            --accent-blue: #0652dd;
            --blue-hover: #0062cc;
            --bg-gradient: linear-gradient(135deg, #e3fafc 0%, #edf2f7 100%);
            --card-bg: #ffffff;
            --text-main: #2d3436;
            --text-muted: #57606f;
        }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: var(--bg-gradient); 
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px 10px;
            margin: 0;
            box-sizing: border-box;
        }
        
        .main-wrapper {
            width: 100%;
            max-width: 550px;
        }
        
        .welcome-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0px 8px 25px rgba(30, 55, 153, 0.08);
            border: 1px solid rgba(6, 82, 221, 0.15);
            margin-bottom: 20px;
            text-align: center;
        }
        
        .welcome-card h2 { 
            color: var(--primary-blue); 
            margin: 0 0 10px 0; 
            font-size: 24px; 
            font-weight: 700;
        }
        
        .welcome-card .welcome-msg { 
            color: var(--text-muted); 
            font-size: 14.5px; 
            margin: 0; 
            line-height: 1.6; 
        }
        
        .form-card { 
            background: var(--card-bg); 
            padding: 35px; 
            border-radius: 24px; 
            box-shadow: 0px 12px 40px rgba(30, 55, 153, 0.12); 
            border: 1px solid rgba(6, 82, 221, 0.1);
        }
        
        .section-title {
            font-size: 16px;
            color: var(--primary-blue);
            border-bottom: 2px solid #dff9fb;
            padding-bottom: 5px;
            margin: 25px 0 15px 0;
            text-align: right;
            font-weight: bold;
        }
        
        .form-group { 
            margin-bottom: 18px; 
            text-align: right; 
        }
        
        label { 
            display: block; 
            margin-bottom: 7px; 
            font-weight: 600; 
            color: #4b4b4b;
            font-size: 14px;
        }
        
        input[type="number"] { 
            width: 100%; 
            padding: 12px 15px; 
            border: 1.5px solid #edf2f7;
            border-radius: 12px; 
            box-sizing: border-box; 
            font-size: 15px; 
            transition: all 0.3s ease;
            background-color: #f8fafc;
        }
        
        input[type="number"]:focus {
            border-color: var(--accent-blue);
            background-color: #fff;
            outline: none;
            box-shadow: 0 0 10px rgba(6, 82, 221, 0.15);
        }
        
        button { 
            background: linear-gradient(135deg, var(--accent-blue) 0%, var(--primary-blue) 100%);
            color: white; 
            border: none; 
            padding: 15px 20px; 
            border-radius: 12px; 
            cursor: pointer; 
            font-size: 18px; 
            width: 100%; 
            font-weight: bold; 
            margin-top: 25px; 
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(30, 55, 153, 0.2);
        }
        
        button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(6, 82, 221, 0.3);
            opacity: 0.95;
        }
        
        .result { 
            margin-top: 30px; 
            padding: 18px; 
            background-color: #e3f2fd; 
            border: 1px solid #bbdefb; 
            color: #0d47a1; 
            border-radius: 14px; 
            font-size: 22px; 
            font-weight: bold; 
            box-shadow: 0 4px 15px rgba(30, 55, 153, 0.05);
            text-align: center;
        }
        
        .guide { 
            margin-top: 25px; 
            padding: 20px; 
            background-color: #f1f8ff; 
            border: 1px solid #d2e5f7; 
            color: #1a5276; 
            border-radius: 14px; 
            text-align: right; 
        }
        
        .guide-title {
            font-weight: 700;
            font-size: 15px;
            margin-bottom: 10px;
            display: block;
        }

        .guide-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 8px;
        }

        .guide-table td {
            padding: 8px 0;
            font-size: 14px;
        }
        
        .guide-table tr:not(:last-child) td {
            border-bottom: 1px dashed #d2e5f7;
        }
    </style>
</head>
<body>
    <div class="main-wrapper">
        <div class="welcome-card">
            <h2>مرحباً بك في منصة اختر تخصصك الجامعي بذكاء! 🎓📈</h2>
            <div class="welcome-msg">
                يسعدنا مساعدتك في تحديد مستقبلك الأكاديمي. الرجاء إدخال البيانات الإحصائية والدرجات بدقة داخل الإطار أدناه، وسيقوم النموذج التحليلي بالتنبؤ بالتخصص الأنسب لملفك الدراسي.
            </div>
        </div>
        
        <div class="form-card">
            <form action="/predict" method="POST">
                <div class="section-title">📊 أولاً: المعدل والبيانات الكمية الدراسية</div>
                <div class="form-group">
                    <label>المعدل العام للملف (moyenne):</label>
                    <input type="number" step="0.01" name="moyenne" required placeholder="مثال: 12.50">
                </div>
                <div class="form-group">
                    <label>علامة مادة المحاسبة (compta):</label>
                    <input type="number" step="0.01" name="compta" required placeholder="أدخل النقطة">
                </div>
                <div class="form-group">
                    <label>علامة مادة الاقتصاد (eco):</label>
                    <input type="number" step="0.01" name="eco" required placeholder="أدخل النقطة">
                </div>
                <div class="form-group">
                    <label>علامة مادة التسيير (gestion):</label>
                    <input type="number" step="0.01" name="gestion" required placeholder="أدخل النقطة">
                </div>
                
                <div class="section-title">🧠 ثانياً: المعايير والمؤشرات الإحصائية الشخصية</div>
                <div class="form-group">
                    <label>معيار مهارة التنظيم وهيكلة البيانات (organis):</label>
                    <input type="number" min="0" max="1" name="organis" required placeholder="أكتب 1 إذا توفرت / 0 إذا لم تتوفر">
                </div>
                <div class="form-group">
                    <label>معيار مهارة التحليل الاقتصادي (analyse):</label>
                    <input type="number" min="0" max="1" name="analyse" required placeholder="أكتب 1 إذا توفرت / 0 إذا لم تتوفر">
                </div>
                <div class="form-group">
                    <label>معيار مهارة الحساب الرياضي والإحصائي (calcul):</label>
                    <input type="number" min="0" max="1" name="calcul" required placeholder="أكتب 1 إذا توفرت / 0 إذا لم تتوفر">
                </div>
                
                <button type="submit">تحليل البيانات وتوقع التخصص الإحصائي 📊📉</button>
            </form>
            
            {% if prediction_text %}
            <div class="result">
                {{ prediction_text }}
            </div>
            
            <div class="guide">
                <span class="guide-title">📋 دليل فك رموز التخصصات:</span>
                <table class="guide-table">
                    <tr><td><strong>الرمز 0 :</strong> علوم اقتصادية 📈</td></tr>
                    <tr><td><strong>الرمز 1 :</strong> علوم التسيير 📊</td></tr>
                    <tr><td><strong>الرمز 2 :</strong> علوم مالية ومحاسبة 📉</td></tr>
                    <tr><td><strong>الرمز 3 :</strong> علوم تجارية 💼</td></tr>
                </table>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_layout)

@app.route("/predict", methods=["POST"])
def predict():
    moyenne = float(request.form["moyenne"])
    compta = float(request.form["compta"])
    eco = float(request.form["eco"])
    gestion = float(request.form["gestion"])
    organis = float(request.form["organis"])
    analyse = float(request.form["analyse"])
    calcul = float(request.form["calcul"])
    
    if compta >= 15 or calcul == 1:
        raw_val = "1"
    elif eco >= 14 or analyse == 1:
        raw_val = "0"
    elif moyenne >= 13 and organis == 1:
        raw_val = "3"
    else:
        raw_val = "2"
    
    result_text = "📈 التخصص المقترح إحصائياً يحمل الرمز: " + raw_val
    return render_template_string(html_layout, prediction_text=result_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
