from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# Add the reCAPTCHA secret key configuration here
app.config['RECAPTCHA_SECRET_KEY'] = 'YOUR_SECRET_KEY'

@app.route('/', methods=['GET', 'POST'])
def verification():
    error_message = None

    if request.method == 'POST':
        doc_hash = request.form['docHash']
        doc_egn = request.form['docEgn']
        recaptcha_response = request.form['g-recaptcha-response']

        # Check if both fields are filled
        if not doc_hash or not doc_egn:
            error_message = "Грешка при решаване на задачата!"
        else:
            # Check if the values are present in the files
            if not check_value_in_file(doc_hash, 'code.txt') or not check_value_in_file(doc_egn, 'egn.txt'):
                error_message = "Грешка при решаване на задачата!"
            else:
                # Verify reCAPTCHA response (you can use the verify_recaptcha function here)
                recaptcha_result = verify_recaptcha(recaptcha_response)

                if not recaptcha_result:
                    error_message = "reCAPTCHA verification failed. Please try again."
                else:
                    # Get the file name based on the ЕГН value
                    file_name = f"{doc_egn}.pdf"
                    try:
                        # Serve the PDF file as a response
                        return send_file(file_name, as_attachment=True)
                    except FileNotFoundError:
                        error_message = "Грешка при решаване на задачата!"

    return render_template('verification.html', error_message=error_message)

def check_value_in_file(value, filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return value in [line.strip() for line in lines]

# Add the verify_recaptcha function here if needed

if __name__ == '__main__':
    app.run(debug=True)
