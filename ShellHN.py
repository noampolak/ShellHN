#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import textwrap
import logging
from logger import logger



# important URLS
HN_url = 'https://news.ycombinator.com/news'
base_comments_URL = 'https://news.ycombinator.com/item?id='


def HNnewsDownloads(url):
    """
     Downloads lists of 40 articles titles sorting by thel rank and
     print them to console
    :param url: The Hacker News URL
    """

    try:
        first30 = requests.get(url+'?p=1')
        second30 = requests.get(url+'?p=2')
        soupFirst30 = BeautifulSoup(first30.content, "lxml")
        soupSecond30 = BeautifulSoup(second30.content, "lxml")
        first_30_articles = soupFirst30.find_all("tr", class_="athing")
        second_30_articles = soupSecond30.find_all("tr", class_="athing")
        for s in range(len(first_30_articles)):
            article_name = first_30_articles[s].find('a', class_="storylink")
            print(f'{s+1}. {article_name.get_text()}')
        for s in range(10):
            article_name = second_30_articles[s].find('a', class_="storylink")
            print(f'{s+31}. {article_name.get_text()}')
    except Exception as e:
        print('Oops,There were a problem: ')
        print(e)
        logger.error(f'error in HNnewsDownloads, error was {e}')


def getArticleItemByRank(article_rank):
    """
     Getting a rank of an article and returns the article item
    :param article_rank: An article rank
    """

    page = int((article_rank-1) / 30) + 1
    HN_article_page = requests.get(HN_url + f'?p={page}')
    HN_article_page_soup = BeautifulSoup(HN_article_page.content, "lxml")
    article_page = HN_article_page_soup.find_all("tr", class_="athing")
    for s in article_page:
        if s.find('span', class_="rank").get_text() == str(article_rank) + '.':
            item = s.get('id')
            return item
    return None

def printComments(article_rank):
    """
     Getting an article_rank id and print it's comments
    :param article_rank: An article rank
    """

    item = getArticleItemByRank(article_rank)
    if item is None:
        print('Article not found')
        return
    try:
        comments_page = requests.get(base_comments_URL+item)
        comments_page_soup = BeautifulSoup(comments_page.content, "lxml")
        comments = comments_page_soup.find_all("tr", class_="comtr")

        for comment in comments:
            comment_ident = int(
                int(comment.find("td", class_="ind").find("img").get("width")) / 10)
            if comment.find("span", class_='commtext').get_text():
                user = comment.find("a", class_='hnuser').get_text()
                age_comment = comment.find(
                    "span", class_='age').find("a").get_text()
                print(textwrap.indent(user + ' ' +
                                      age_comment, createIdent(comment_ident)))
                print(textwrap.indent(comment.find(
                    "span", class_='commtext').get_text(), createIdent(comment_ident)))
                print(' ')
    except Exception as e:
        print('Oops,There were a problem: ')
        print(e)
        logger.error(f'error in printComments article_rank was {article_rank}, article item was {item} and error was {e}')


def createIdent(num=0):
    """
     Getting a number and returns a spaces string with the number size
    :param num: A number
    """

    ident = ''
    for i in range(num):
        ident += ' '
    return ident



def main():
    logger.info('Application started')
    print('Welcome to ShellHN!!!')
    print('Here are the 40 top rank of Hacker News')
    HNnewsDownloads(HN_url)

    while True:
        try:
            rank_number = input(
                "Please enter a number of article rank or 'q' to quit: ")
            if rank_number == 'q':
                break
            rank_number = int(rank_number)
            logger.info(f'calling to printComments for article rank {rank_number}')
            printComments(rank_number)
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    print('Bye!')
    logger.info('Application stopped')


if __name__ == '__main__':
    main()
