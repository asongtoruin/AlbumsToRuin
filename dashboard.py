from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


FA_PATH = r'fonts/Font Awesome 5 Free-Solid-900.otf'
NUM_FONT_PATH = r'fonts/gilroy-extrabold.otf'


def maximise_font_height(font_path, msg, desired_height, start_size=1):
    font_size = start_size
    font = ImageFont.truetype(font_path, font_size)
    while font.getsize(msg)[0] < desired_height:
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)
    return font_size - 1


def draw_dashboard(queue, completed, errors):
    # inky display size
    WIDTH = 212
    HEIGHT = 104

    # Buffer around the edge of the dashboard, and scale for getting better 
    # quality
    BUFFER = 6
    SCALE = 20

    # Scale up
    big_width = WIDTH * SCALE
    big_height = HEIGHT * SCALE
    big_buff = BUFFER * SCALE

    # 3 vertical sections
    section_height = int((big_height - big_buff) / 3)+1

    # Calculating the font height is slow, so let's shortcut it
    # fa_size = maximise_font_height(FA_PATH, u'\uf0c0', section_height)
    fa_size=522

    # Set up the larger image
    img = Image.new(size=(big_width, big_height), color='white', mode='P')
    draw = ImageDraw.Draw(img)

    fa = ImageFont.truetype(FA_PATH, fa_size)

    # Font Awesome unicode for the icons we want to use
    clip = u'\uf46d'
    tick = u'\uf058'
    warn = u'\uf06a'

    # Work out the width of the icons, so we can verically centre them
    clip_width = fa.getsize(clip)[0]
    tick_width = fa.getsize(tick)[0]
    warn_width = fa.getsize(warn)[0]

    v_centre = big_width * .5 + max(clip_width, tick_width, warn_width)/2

    # Draw each icon
    draw.text(
        (v_centre - clip_width/2, big_buff), clip, 
        (0,0,0), font=fa
    )
    draw.text(
        (v_centre - tick_width/2, big_buff+section_height), tick, 
        (0,0,0), font=fa
    )
    draw.text(
        (v_centre - warn_width/2, big_buff+2*section_height), warn, 
        (255,0,0), font=fa
    )

    # Again, slow calcs for the large logo. Bypass. 
    # big_size = maximise_font_height(FA_PATH, u'\uf51f', big_height-2*big_buff)
    big_fa_size = 1898

    big_fa = ImageFont.truetype(FA_PATH, big_fa_size)

    # The icon here is for a record
    draw.text((big_buff,big_buff), u'\uf51f', (0, 0, 0), font=big_fa)

    # We want a nice font for the numbers.
    # num_size = maximise_font_height(NUM_FONT_PATH, '999', section_height)
    num_size = 388
    num_font = ImageFont.truetype(NUM_FONT_PATH, num_size)

    # Work out sizes so we can right-align numbers, then draw them on
    queue_size = num_font.getsize(str(queue))
    completed_size = num_font.getsize(str(completed))
    error_size = num_font.getsize(str(errors))

    draw.text(
        (big_width - big_buff - queue_size[0], big_buff), 
        str(queue), (0,0,0), font=num_font
    )
    draw.text(
        (big_width - big_buff - completed_size[0], big_buff + section_height), 
        str(completed), (0,0,0), font=num_font
    )
    draw.text(
        (big_width - big_buff - error_size[0], big_buff + section_height*2), 
        str(errors), (255,0,0), font=num_font
    )

    return img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
