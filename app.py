from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'  # only used for flash messages

db = SQLAlchemy(app)

STATUS_CHOICES = ['Applied', 'Interviewing', 'Offer', 'Rejected', 'Withdrawn']


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Applied')
    date_applied = db.Column(db.Date, nullable=False, default=date.today)
    follow_up_date = db.Column(db.Date, nullable=True)
    job_url = db.Column(db.String(300), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').date()


@app.route('/')
def index():
    status_filter = request.args.get('status', '')
    query = Application.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    applications = query.order_by(Application.date_applied.desc()).all()

    total = Application.query.count()
    counts = {
        s: Application.query.filter_by(status=s).count() for s in STATUS_CHOICES
    }

    return render_template(
        'index.html',
        applications=applications,
        status_choices=STATUS_CHOICES,
        current_filter=status_filter,
        total=total,
        counts=counts,
        today=date.today(),
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        company = request.form.get('company', '').strip()
        position = request.form.get('position', '').strip()

        if not company or not position:
            flash('Company and position are required.', 'error')
            return render_template('form.html', form_data=request.form, status_choices=STATUS_CHOICES, mode='add')

        application = Application(
            company=company,
            position=position,
            status=request.form.get('status', 'Applied'),
            date_applied=parse_date(request.form.get('date_applied')) or date.today(),
            follow_up_date=parse_date(request.form.get('follow_up_date')),
            job_url=request.form.get('job_url', '').strip(),
            notes=request.form.get('notes', '').strip(),
        )
        db.session.add(application)
        db.session.commit()
        flash(f'Added application for {position} at {company}.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', form_data={}, status_choices=STATUS_CHOICES, mode='add')


@app.route('/edit/<int:app_id>', methods=['GET', 'POST'])
def edit(app_id):
    application = Application.query.get_or_404(app_id)

    if request.method == 'POST':
        company = request.form.get('company', '').strip()
        position = request.form.get('position', '').strip()

        if not company or not position:
            flash('Company and position are required.', 'error')
            return render_template('form.html', form_data=request.form, status_choices=STATUS_CHOICES, mode='edit', app_id=app_id)

        application.company = company
        application.position = position
        application.status = request.form.get('status', 'Applied')
        application.date_applied = parse_date(request.form.get('date_applied')) or date.today()
        application.follow_up_date = parse_date(request.form.get('follow_up_date'))
        application.job_url = request.form.get('job_url', '').strip()
        application.notes = request.form.get('notes', '').strip()

        db.session.commit()
        flash(f'Updated application for {position} at {company}.', 'success')
        return redirect(url_for('index'))

    form_data = {
        'company': application.company,
        'position': application.position,
        'status': application.status,
        'date_applied': application.date_applied.isoformat() if application.date_applied else '',
        'follow_up_date': application.follow_up_date.isoformat() if application.follow_up_date else '',
        'job_url': application.job_url,
        'notes': application.notes,
    }
    return render_template('form.html', form_data=form_data, status_choices=STATUS_CHOICES, mode='edit', app_id=app_id)


@app.route('/delete/<int:app_id>', methods=['POST'])
def delete(app_id):
    application = Application.query.get_or_404(app_id)
    db.session.delete(application)
    db.session.commit()
    flash(f'Deleted application for {application.position} at {application.company}.', 'success')
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
