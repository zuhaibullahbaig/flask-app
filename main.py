from flask import Flask, request, render_template, redirect, send_file
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os
from datetime import datetime, timedelta


from short_code import generate_unique_short_code
from urllib.parse import urlparse

def get_domain_name(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Extract and return the domain name
    return parsed_url.netloc

def is_valid_url(text):
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anonminion@localhost/chotu'
db = SQLAlchemy(app)

# DATABASE STUFF 
def delete_expired_custom_urls():
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    custom_urls_to_delete = ShortURL.query.filter(
        ShortURL.url_type == 'custom',
        ShortURL.created_at < thirty_days_ago
    ).all()

    for url in custom_urls_to_delete:
        db.session.delete(url)

    db.session.commit()


class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(40), unique=True, nullable=False)
    click_count = db.Column(db.Integer, default=0)
    fb_click_count = db.Column(db.Integer, default=0)
    twitter_click_count = db.Column(db.Integer, default=0)
    instagram_click_count = db.Column(db.Integer, default=0)
    others_click_count = db.Column(db.Integer, default=0)
    url_type = db.Column(db.Enum('custom', 'automated'), nullable=False)

class LinkInBio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    click_count = db.Column(db.Integer, default=0)
    links = db.Column(db.JSON, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    template_name = db.Column(db.Enum('template_1', 'template_2', 'template_3', 'template_4', 'template_5'), nullable=False)


with app.app_context():
    db.create_all()


# CLEARNING QR CODES AFTER 5 MINUTES

qr_code_directory = 'static/images/qrcodes'

# Function to delete QR codes older than 5 minutes
def cleanup_qr_codes():
    five_minutes_ago = datetime.now() - timedelta(minutes=5)
    for filename in os.listdir(qr_code_directory):
        file_path = os.path.join(qr_code_directory, filename)
        file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if file_creation_time < five_minutes_ago:
            os.remove(file_path)
            print('removed file')


#BASIC ROUTES 

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/')
@app.route('/home')
def second():
    return render_template('index.html')

@app.route('/terms')
def terms():
    return render_template('termsofuse.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/blog')
def blog():
    return render_template('blogs/blog.html')


@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/about')
def about():
    return render_template('about.html')



# Link In Bios
@app.route('/onelinks')
def onelinks():
    return render_template('linkinbios/intro.html')

@app.route('/o/<link_code>')
def access_onelink(link_code):
        link_in_one = LinkInBio.query.filter_by(code=link_code).first()
        if link_in_one:
            name = link_in_one.name
            description = link_in_one.description
            template_name = link_in_one.template_name
            data = link_in_one.links
            access_file = f"/static/images/profiles/{link_code}.png"
            if template_name == 'template_1':
                return render_template('linkinbios/style_one.html', data={'links': data, "name":name,"access_file":access_file, "description":description,})
            elif template_name == 'template_2':
                return render_template('linkinbios/style_two.html', data={'links': data, "name":name, "access_file":access_file, "description":description, })
            elif template_name == 'template_3':
                return render_template('linkinbios/style_three.html', data={'links': data, "name":name, "access_file":access_file, "description":description,})
            elif template_name == 'template_5':
                return render_template('linkinbios/style_five.html', data={'links': data, "name":name, "access_file":access_file, "description":description, })
            else:
                return render_template('linkinbios/style_four.html', data={'links': data, "name":name, "access_file":access_file, "description":description, })
        return render_template('error.html')

@app.route('/onelinks/generator', methods=['POST', 'GET'])
def onlinks_generator():
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            image = request.files['profile-image']
            template_name = request.form['template_name']
            noofcount = int(request.form['noofcount'])
            first_link_name = request.form['link_one_name']      
            first_link_url = request.form['link_one_url']             
            second_link_name = request.form['link_two_name']
            second_link_url = request.form['link_two_url']
            third_link_name = request.form['link_three_name']
            third_link_url = request.form['link_three_url']
            if noofcount >= 1:
                fourth_link_name = request.form['link-four-name']
                fourth_link_url = request.form['link-four-url']
                if noofcount >= 2:
                    fifth_link_name = request.form['link-five-name']
                    fifth_link_url = request.form['link-five-url']
                    if noofcount == 3:
                        sixth_link_name = request.form['link-six-name']
                        sixth_link_url = request.form['link-six-url']
            else:
                pass
            if noofcount == 0:
                data = {
                    first_link_name: first_link_url,
                    second_link_name: second_link_url,
                    third_link_name: third_link_url,               
                }
            elif noofcount == 1:
                data = {
                    first_link_name: first_link_url,
                    second_link_name: second_link_url, 
                    third_link_name: third_link_url,
                    fourth_link_name: fourth_link_url, }
            elif noofcount == 2:
                data = {
                    first_link_name: first_link_url,
                    second_link_name: second_link_url,
                    third_link_name: third_link_url,
                    fourth_link_name: fourth_link_url,
                    fifth_link_name: fifth_link_url,
                }
            elif noofcount >= 3:
                data = {
                    first_link_name: first_link_url,
                    second_link_name: second_link_url,
                    third_link_name: third_link_url,
                    fourth_link_name: fourth_link_url,
                    fifth_link_name: fifth_link_url,
                    sixth_link_name: sixth_link_url                
                }
            

            code = generate_unique_short_code()
            image_name = f'{code}.png'
            destination = os.path.join('static', 'images', 'profiles', image_name)
            image.save(destination)

            new_item = LinkInBio(
                code=code,
                links=data,
                name=name,
                description=description,
                template_name=template_name,
            )
            db.session.add(new_item)
            db.session.commit()        

            url = f"http://localhost:8000/o/{code}"
            return render_template('generated_onelink.html', data={'url': url})
        except Exception as Er:
            print(Er)
            return render_template('onelinks.html')
    return render_template('onelinks.html')

@app.route('/onelinks/template_one')
def template_one():
    return render_template('linkinbios/style_one.html')

@app.route('/onelinks/template_two')
def template_two():
    return render_template('linkinbios/style_two.html')

@app.route('/onelinks/template_three')
def template_three():
    return render_template('linkinbios/style_three.html')

@app.route('/onelinks/template_four')
def template_four():
    return render_template('linkinbios/style_four.html')


@app.route('/onelinks/template_five')
def template_five():
    return render_template('linkinbios/style_five.html')





# SHORTENING CODE 
@app.route('/qrcodegenerator/url')
def urlqrcode():
    return render_template('qrcodegenerator/urlqrcode.html')

@app.route('/qrcodegenerator/contact_qr')
def contactqrcode():
    return render_template('qrcodegenerator/contact_qr.html')


@app.route('/qrcodegenerator/sms_qr', methods=['GET'])
def sms_qr():
    return render_template('qrcodegenerator/sms_qr.html')


@app.route('/qrcodegenerator/email_qr')
def email_qr():
    return render_template('qrcodegenerator/email_qr.html')



@app.route('/qrcodegenerator/location_qr')
def location_qr():
    return render_template('qrcodegenerator/location_qr.html')


@app.route('/qrcodegenerator/event_qr')
def event_qr():
    return render_template('qrcodegenerator/event_qr.html')


@app.route('/qrcodegenerator/wifi_qr')
def wifi_qr():
    return render_template('qrcodegenerator/wifi_qr.html')

@app.route('/qrcodegenerator')
def qrcodegenerator():
    return render_template('qrcode.html')


# QRkfjaklsjf
@app.route('/custom', methods=['GET', 'POST'])
def custom():
    if request.method == 'POST':
        restricted = ['home', 'faqs', 'qrcode', 'qrcodegenerator', 'login', 'signup', 'shorten', 'custom', 'shortener', 'c', 'error', 'o', 'onelinks', 'about', 'privacy', 'terms', 'contact', 'faqs', 'blog', 'products', ' ', '', '  ']
        custom_url = request.form['custom-url']
        short_url = ShortURL.query.filter_by(short_code=custom_url).first()
        custom = f"/{custom_url}"
        if short_url:
            return render_template('custom.html', message=f'{custom} not available', red='6')
        elif custom_url in restricted:
            return render_template('custom.html', message=f'{custom} not available', red='6')
        else:
            return render_template('custom.html', data=f'/custom/create{custom}', message=f'{custom} is available', green='6')
    return render_template('custom.html', message='', green='d')

#CUSTOM URL
@app.route('/custom/create/<short_code>', methods=['GET', 'POST'])
def createcustom(short_code):
    restricted = ['home', 'qrcode', 'qrcodegenerator', 'login', 'signup', 'shorten', 'custom', 'shortener', 'c', 'error', 'o', 'onelinks', 'about', 'privacy', 'terms', 'contact', 'faqs', 'blog', 'products', ' ', '', '  ']
    short = ShortURL.query.filter_by(short_code=short_code).first()
    
    if short or short_code in restricted:
        return render_template('custom.html', message=f'/{short_code} is not available', red='d')
    custom_url = f'/custom/create/{short_code}'
    link_url = f"http://localhost:8000/{short_code}"
    link_analytics_url = f"http://localhost:8000c/{short_code}"
    if request.method == 'POST':
        dest_url = request.form['dest-url']
        if is_valid_url(dest_url):
            custom_url = f'/custom/create/{short_code}'
            link_url = f"http://localhost:8000/{short_code}"
            link_analytics_url = f"http://localhost:8000/c/{short_code}"
            short_url = ShortURL(original_url=dest_url, short_code=short_code, url_type="custom")
            try:
                db.session.add(short_url)
                db.session.commit()
                print(dest_url)
            except Exception as Ex:
                print(Ex)
            return render_template('created_custom.html', message='We have set your custom backlink to the destination url.  Your link will expire in 30 Days', link_url=link_url, link_analytics_url=link_analytics_url)
        else:
            return render_template('customurl.html', link_url=link_url, link_analytics_url=link_analytics_url, custom_url=custom_url, warning='check your url, it appears to be wrong')
    print(short_code)
    
    return render_template('customurl.html', link_url=link_url, link_analytics_url=link_analytics_url, custom_url=custom_url)


# AUTOMATIC URL
@app.route('/shorten', methods=['POST', 'GET'])
def shortener():
    if request.method == 'POST':
        if is_valid_url(request.form['link']) != True:
            link_url = "Paste/Write-a-correct-url"
            messages = {'link': link_url,
                        'message': "wrong url"}
            
            return render_template('shortener.html', message=messages)
    
        link_url = request.form['link']
        messages = {'link': link_url}
        while True:
            short_code = generate_unique_short_code()
            short_url = ShortURL(original_url=link_url, short_code=short_code, url_type="automated")
            try:
                db.session.add(short_url)
                db.session.commit()
                new_url = f'http://localhost:8000/{short_code}'
                link_stats_url = f"http://localhost:8000/c/{short_code}"
                data = {'new_url': new_url, 'link':link_url, 'link_stats': link_stats_url}
                return render_template('shortener.html', message=data)
            
            except IntegrityError:
                db.session.rollback()

    messages = {'link': "Write/Paste-a-correct-url"}
            
    return render_template('shortener.html', message=messages)




# LINK STATISTICS 



@app.route('/c/<link_code>')
def get_click_count_and_date(link_code):
    short_url = ShortURL.query.filter_by(short_code=link_code).first()

    if short_url:
        click_count = short_url.click_count
        original_url = short_url.original_url
        creation_date = short_url.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Format the date
        fb_count = short_url.fb_click_count
        twitter_count = short_url.twitter_click_count
        ig_count = short_url.instagram_click_count
        other_count = short_url.others_click_count
        
        fb_percentage = 0;
        ig_percentage = 0;
        twitter_percentage = 0;
        other_percentage = 0;

        if fb_count != 0:
            fb_percentage = fb_count / click_count * 100
            fb_percentage = round(fb_percentage, 2)
        if twitter_count != 0:
            twitter_percentage = twitter_count / click_count * 100
            twitter_percentage = round(twitter_percentage, 2)
        if ig_count != 0:
            ig_percentage = ig_count / click_count * 100
            ig_percentage = round(ig_percentage, 2)
        if other_count != 0:
            other_percentage = other_count / click_count * 100
            other_percentage = round(other_percentage, 2)
            
        data = {
            'ig_count' : ig_count,
            'ig_percentage': ig_percentage,
            'twitter_count': twitter_count,
            'twitter_percentage': twitter_percentage,
            'fb_count': fb_count,
            'fb_percentage': fb_percentage,
            'other_count': other_count,
            'other_percentage': other_percentage,
        }

        return render_template('click_info.html', click_count=click_count, creation_date=creation_date, original_url=original_url, other_data=data)
    else:
        return render_template('error.html')
    


@app.route('/<url_code>')
def redirect_to_original(url_code):
    short_url = ShortURL.query.filter_by(short_code=url_code).first()

    if short_url:
        short_url.click_count += 1
        referer = request.headers.get('Referer')
        domain = str(get_domain_name(referer))
        
        if 'facebook' in domain:
            short_url.fb_click_count += 1

            print('facebook')
        elif 'instagram' in domain:
            short_url.instagram_click_count += 1
            print('instagram')

        elif 'twitter' in domain or 'x.com' in domain:
            short_url.twitter_click_count += 1
            print('twitter')

        else:
            short_url.others_click_count += 1
            print(short_url.others_click_count)
            print('others')
        db.session.commit()

        return redirect(short_url.original_url)
    else:
        return render_template('error.html')
    

@app.errorhandler(404)
def error(er):
    return render_template('error.html')

@app.errorhandler(500)
def err500(er):
    return render_template('500error.html')

if __name__ == "__main__":

    app.run(debug=True, port=10001)
