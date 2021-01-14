# Credit: https://juejin.cn/post/6916713099256922120
import requests
from pyecharts.charts import Bar
from pyecharts import options as opts


def get_data(language, year, number):
    base_url = f'https://api.github.com/search/repositories' \
               f'?q=language:{language}+created:%3E{year - 1}-12-31&sort=stars&order=desc&per_page={number}'
    response = requests.get(base_url)
    result = response.json()
    data = {}
    for item in result['items']:
        data[item['name']] = [item['html_url'], item['stargazers_count'], item['watchers_count'], item['forks']]
    return data


def show_img(data, language, year, number):
    filename = f"{language}-{year}-{number}.html"
    names = list(data.keys())
    values = [data[name][1] for name in names]
    bar = Bar()
    bar.add_xaxis(names[::-1])
    bar.add_yaxis("star", values[::-1])
    bar.reversal_axis()
    bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
    bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(name_rotate=0, name="Repo", axislabel_opts={'interval': -10, "rotate": 0}),
        title_opts=opts.TitleOpts(title=f"{year} GitHub {language.capitalize()} TOP {number}"))
    bar.render(path=f"./generated/{filename}")


def main():
    languages = ['javascript', 'python', 'cpp', 'go', 'html']
    years = [2018, 2019, 2020]
    number = 20
    for language in languages:
        for year in years:
            data = get_data(language, year, number)
            show_img(data, language, year, number)


if __name__ == '__main__':
    main()
