from flask import Flask, render_template_string, request, redirect, url_for
import datetime

app = Flask(__name__)

exam_info = {
    'module_name': 'Sample Module',
    'num_students': 0,
    'start_time': '10:00',
    'end_time': '12:00',
    'leave_time': '10:30',
    'issues': [],
    'notes': '',
}

@app.route("/", methods=["GET", "POST"])
def stopwatch():
    if request.method == "POST":
        exam_info['start_time'] = request.form['start_time']
        exam_info['end_time'] = request.form['end_time']
        exam_info['leave_time'] = request.form['leave_time']
        exam_info['num_students'] = request.form['num_students']
        return redirect(url_for('stopwatch'))

    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Exam Stopwatch</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                padding: 20px;
            }

            .container {
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: auto;
                text-align: center;
            }

            h2 {
                margin: 10px 0;
            }

            input[type="time"], input[type="number"], input[type="submit"] {
                font-size: 18px;
                padding: 10px 20px;
                margin: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }

            input[type="submit"] {
                background-color: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }

            #time-display {
                font-size: 48px;
                margin: 20px 0;
            }

            .alert {
                font-size: 24px;
                margin-top: 20px;
            }

            .alert-green {
                color: green;
            }

            .notes {
                text-align: left;
                margin-top: 20px;
            }

            textarea {
                width: 100%;
                height: 100px;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
            }

            .notes ul {
                list-style-type: none;
                padding: 0;
            }

            .notes li {
                background: #f9f9f9;
                padding: 10px;
                border-radius: 5px;
                margin: 5px 0;
                border: 1px solid #ccc;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>EXAM STOPWATCH</h2>
            <p>Current Time: <strong id="current-time">{{ current_time }}</strong></p>
            <p>Current Date: <strong id="current-date">{{ current_date }}</strong></p>
            <form method="POST">
                <label for="start-time">Start Time:</label>
                <input type="time" id="start-time" name="start_time" value="{{ start_time }}"><br>
                <label for="end-time">End Time:</label>
                <input type="time" id="end-time" name="end_time" value="{{ end_time }}"><br>
                <label for="leave-time">Leave Time:</label>
                <input type="time" id="leave-time" name="leave_time" value="{{ leave_time }}"><br>
                <label for="num-students">Number of Students:</label>
                <input type="number" id="num-students" name="num_students" value="{{ num_students }}"><br>
                <input type="submit" value="Update Exam Details">
            </form>
            <div id="time-display">00:00:00</div>
            <div id="alerts" class="alert"></div>
            <div class="notes">
                <h3>Notes</h3>
                <form action="{{ url_for('add_note') }}" method="POST">
                    <textarea name="note"></textarea><br>
                    <input type="submit" value="Add Note">
                </form>
                <ul>
                    {% for issue in issues %}
                        <li>{{ issue }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>

        <script>
            var startTime, endTime, leaveTime, timer;
            var currentTime = 0;

            document.addEventListener("DOMContentLoaded", function() {
                startTime = '{{ start_time }}';
                endTime = '{{ end_time }}';
                leaveTime = '{{ leave_time }}';
                checkExamStart();
                setInterval(updateClock, 1000); // Update clock every second
            });

            function updateClock() {
                var now = new Date();
                var hours = now.getHours();
                var minutes = now.getMinutes();
                var seconds = now.getSeconds();
                var ampm = hours >= 12 ? 'PM' : 'AM';
                hours = hours % 12;
                hours = hours ? hours : 12; // the hour '0' should be '12'
                var currentTimeStr = hours.toString().padStart(2, '0') + ':' + 
                                     minutes.toString().padStart(2, '0') + ':' + 
                                     seconds.toString().padStart(2, '0') + ' ' + ampm;
                document.getElementById('current-time').innerText = currentTimeStr;

                var currentDateStr = (now.getDate()).toString().padStart(2, '0') + '/' +
                                     (now.getMonth() + 1).toString().padStart(2, '0') + '/' +
                                     now.getFullYear();
                document.getElementById('current-date').innerText = currentDateStr;
            }

            function updateDisplay() {
                var hours = Math.floor(currentTime / 3600);
                var minutes = Math.floor((currentTime % 3600) / 60);
                var seconds = currentTime % 60;
                document.getElementById('time-display').innerText = 
                    hours.toString().padStart(2, '0') + ':' +
                    minutes.toString().padStart(2, '0') + ':' +
                    seconds.toString().padStart(2, '0');
            }

            function updateAlerts() {
                var now = new Date();
                var alertsDiv = document.getElementById('alerts');
                alertsDiv.innerHTML = '';

                var currentTimeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                                     now.getMinutes().toString().padStart(2, '0');

                if (currentTimeStr >= leaveTime && currentTimeStr <= endTime) {
                    var leaveTime12hr = formatTimeTo12hr(leaveTime);
                    alertsDiv.innerHTML = '<span class="alert-green">You can leave the room from ' + leaveTime12hr + '</span>';
                } else {
                    var leaveTime12hr = formatTimeTo12hr(leaveTime);
                    alertsDiv.innerHTML = '<span class="alert-green">You can leave the room from ' + leaveTime12hr + '</span>';
                }
            }

            function formatTimeTo12hr(timeStr) {
                var timeParts = timeStr.split(':');
                var hours = parseInt(timeParts[0]);
                var minutes = timeParts[1];
                var ampm = hours >= 12 ? 'PM' : 'AM';
                hours = hours % 12;
                hours = hours ? hours : 12; // the hour '0' should be '12'
                return hours.toString().padStart(2, '0') + ':' + minutes + ' ' + ampm;
            }

            function startTimer() {
                if (!timer) {
                    timer = setInterval(function () {
                        currentTime++;
                        updateDisplay();
                        updateAlerts();
                        
                        var now = new Date();
                        var currentTimeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                                             now.getMinutes().toString().padStart(2, '0');
                        if (currentTimeStr === endTime) {
                            stopTimer();
                            alert('Exam has ended!');
                        }
                    }, 1000);
                }
            }

            function stopTimer() {
                clearInterval(timer);
                timer = null;
            }

            function resetTimer() {
                currentTime = 0;
                updateDisplay();
                updateAlerts();
                stopTimer();
            }

            function checkExamStart() {
                var now = new Date();
                var currentTimeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                                     now.getMinutes().toString().padStart(2, '0');
                if (currentTimeStr === startTime) {
                    startTimer();
                    alert('Exam has started!');
                }
                else {
                    setTimeout(checkExamStart, 1000);
                }
            }

            updateDisplay();
            updateAlerts();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content,
                                  start_time=exam_info['start_time'], end_time=exam_info['end_time'],
                                  leave_time=exam_info['leave_time'], num_students=exam_info['num_students'],
                                  current_time=current_time, current_date=current_date,
                                  issues=exam_info['issues'])

@app.route("/add_note", methods=["POST"])
def add_note():
    note = request.form.get('note')
    if note:
        exam_info['issues'].append(note)
    return redirect(url_for('stopwatch'))

if __name__ == "__main__":
    app.run(debug=True)
