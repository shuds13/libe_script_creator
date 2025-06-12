from flask import Flask, request, render_template, send_file
import jinja2
import os

app = Flask(__name__)

@app.route('/generators.json')
def serve_generators():
    return send_file('data/generators.json')

@app.route('/', methods=['GET', 'POST'])
def index():
    script = None
    simf_script = None
    download_link = None
    simf_link = None

    if request.method == 'POST':

        app_ref = request.form.get('app_ref', '')

        # Manager fields
        num_workers = request.form.get('num_workers', type=int)
        sim_app = request.form.get('sim_app', '')
        input_file = request.form.get('input_file', '')
        gen_module = request.form.get('gen_module')
        gen_function = request.form.get('gen_function')

        # Worker fields
        nodes = request.form.get('nodes', type=int)
        procs = request.form.get('procs', type=int)

        # Render run_libe.py
        template_path = os.path.join(app.root_path, 'templates', 'run_libe.py.j2')
        with open(template_path) as f:
            template = jinja2.Template(f.read())
        script = template.render(gen_module=gen_module,
                                 gen_function=gen_function,
                                 num_workers=num_workers,
                                 sim_app=sim_app,
                                 app_ref=app_ref,
                                 input_file=input_file)

        os.makedirs('static', exist_ok=True)
        output_path = os.path.join('static', 'run_libe.py')
        with open(output_path, 'w') as f:
            f.write(script)
        download_link = '/' + output_path

        # Render simf.py
        simf_template_path = os.path.join(app.root_path, 'templates', 'simf.py.j2')
        with open(simf_template_path) as f:
            simf_template = jinja2.Template(f.read())
        simf_script = simf_template.render(nodes=nodes,
                                           procs=procs,
                                           app_ref=app_ref)

        simf_output_path = os.path.join('static', 'simf.py')
        with open(simf_output_path, 'w') as f:
            f.write(simf_script)
        simf_link = '/' + simf_output_path

    return render_template('index.html',
                           request=request,
                           script=script,
                           download_link=download_link,
                           simf_script=simf_script,
                           simf_link=simf_link)

if __name__ == '__main__':
    app.run(debug=True)
