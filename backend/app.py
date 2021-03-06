from flask import Flask, render_template, request, url_for

from backend.scrapers import get_html
from backend.scrapers.downloadable import get_downloadable
from backend.scrapers.events import event_page_link, get_top_event
from backend.scrapers.footer import get_footer
from backend.scrapers.news import get_all_news, get_top_news, news_page_link
from backend.scrapers.notice import get_all_notice, get_top_notice, notice_page_link
from backend.utils import get_navbar
from backend.scrapers.detail_html import get_responsive_html


app = Flask(__name__)


@app.route("/")
def home():
    html = get_html(cache=True)
    top_notice = get_top_notice(html)
    notice_link = notice_page_link(html)
    top_events = get_top_event(html)
    event_link = event_page_link(html)
    top_news = get_top_news(html)
    news_link = news_page_link(html)

    top_items = {
        "Notice": {"link": notice_link, "list": top_notice, "detail_func": "notice"},
        "News": {"link": news_link, "list": top_news, "detail_func": "notice"},
        "Events": {"link": event_link, "list": top_events, "detail_func": "notice"},
    }

    main_navs, nested_navs, footer = get_layout_data(html)
    return render_template(
        "home.html",
        top_items=top_items,
        footer=footer,
        nested_navs=nested_navs,
        main_navs=main_navs,
    )


def get_layout_data(html):
    footer = get_footer(html)
    main_navs, nested_navs = get_navbar(html)
    return (main_navs, nested_navs, footer)


@app.route("/notice")
def notice():
    html = get_html(cache=True)
    main_navs, nested_navs, footer = get_layout_data(html)
    top_notices = get_top_notice(html)
    link = request.args.get("link", "", type=str)
    if not link:
        pass

    html = get_responsive_html(link)

    return render_template(
        "detail.html",
        title="Notice",
        html=html,
        main_navs=main_navs,
        nested_navs=nested_navs,
        footer=footer,
    )
