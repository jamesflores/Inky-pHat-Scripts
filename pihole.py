import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto


# Replace this with your Pi-hole IP address or domain name and API key
PIHOLE_URL = 'http://xxx.xxx.xxx.xxx/admin/api.php'
API_KEY = '...'

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def main():
    data = get_pihole_stats()
    
    # Extract the relevant data
    dns_queries_today = format(data['dns_queries_today'], ',')
    ads_percentage = data['ads_percentage_today']

    text = f"Pi-hole Stats Today Queries: {dns_queries_today} Ads Blocked: {ads_percentage:.2f}%"
    draw_centered_text(text, FONT_PATH, rotate=180, font_size=20)


def get_pihole_stats():
    params = {
        'summaryRaw': '',  # This returns a more detailed set of data
        'auth': API_KEY
    }

    try:
        response = requests.get(PIHOLE_URL, params=params)
        response.raise_for_status()  # Raises an error for bad HTTP status codes
        data = response.json()
        #data = {
        #    'domains_being_blocked': 248942,
        #    'dns_queries_today': 120817,
        #    'ads_blocked_today': 9577,
        #    'ads_percentage_today': 7.926865,
        #    'unique_domains': 3512,
        #    'queries_forwarded': 75373,
        #    'queries_cached': 32555,
        #    'clients_ever_seen': 10,
        #    'unique_clients': 10,
        #    'dns_queries_all_types': 120817,
        #    'reply_UNKNOWN': 5162,
        #    'reply_NODATA': 19576,
        #    'reply_NXDOMAIN': 23246,
        #    'reply_CNAME': 33593,
        #    'reply_IP': 36354,
        #    'reply_DOMAIN': 114,
        #    'reply_RRNAME': 18,
        #    'reply_SERVFAIL': 14,
        #    'reply_REFUSED': 352,
        #    'reply_NOTIMP': 0,
        #    'reply_OTHER': 0,
        #    'reply_DNSSEC': 0,
        #    'reply_NONE': 0,
        #    'reply_BLOB': 2388,
        #    'dns_queries_all_replies': 120817,
        #    'privacy_level': 0,
        #    'status': 'enabled',
        #    'gravity_last_updated': {
        #        'file_exists': True,
        #        'absolute': 1723692150,
        #        'relative': {
        #            'days': 1,
        #            'hours': 20,
        #            'minutes': 35
        #        }
        #    }
        #}
        
        return {
            'ads_blocked_today': data['ads_blocked_today'],
            'dns_queries_today': data['dns_queries_today'],
            'ads_percentage_today': data['ads_percentage_today'],
            'unique_domains': data['unique_domains'],
            'clients_ever_seen': data['clients_ever_seen'],
            #'dns_queries_all_time': data['dns_queries_all_time'],
            'domains_being_blocked': data['domains_being_blocked']
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error querying Pi-hole API: {e}")
        return None


def draw_centered_text(text, font_path, rotate=0, font_size=20):
    # Initialize InkyPHAT
    inky_display = auto()
    inky_display.set_border(inky_display.WHITE)

    # Create a new PIL image
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.WHITE)
    draw = ImageDraw.Draw(img)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Determine maximum width for text wrapping
    max_width = inky_display.HEIGHT - 10 if rotate in (90, 270) else inky_display.WIDTH - 10

    # Wrap the text with dynamic width calculation
    wrapped_text = []
    for i in range(len(text), 0, -1):
        wrapped_text = textwrap.wrap(text, width=i)
        longest_line = max(wrapped_text, key=len)
        bbox = font.getbbox(longest_line)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            break

    # Calculate total height of wrapped text
    bbox = font.getbbox('hg')  # 'hg' accounts for ascenders and descenders
    line_height = bbox[3] - bbox[1]
    total_height = len(wrapped_text) * line_height

    # Calculate starting position to center vertically
    y = (inky_display.HEIGHT - total_height) // 2 if rotate in (0, 180) else (inky_display.WIDTH - total_height) // 2

    # Draw each line of text
    for line in wrapped_text:
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        x = (inky_display.WIDTH - line_width) // 2 if rotate in (0, 180) else (inky_display.HEIGHT - line_width) // 2
        draw.text((x, y), line, inky_display.BLACK, font=font)
        y += line_height

    # Rotate and display the image
    inky_display.set_image(img.rotate(rotate))
    inky_display.show()


if __name__ == '__main__':
    main()


