import os
import sys
import array
import codecs
import statistics

from matplotlib import rc

rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:
    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with codecs.open(filename, encoding='UTF-8') as f:
            (n, _nlinks) = tuple(map(int, f.readline().strip().split()))  # TODO: прочитать из файла
            self._titles = []
            self._num_of_pages = n
            self._sizes = array.array('L', [0] * n)
            self._links = array.array('L', [0] * _nlinks)
            self._redirect = array.array('B', [0] * n)
            self._offset = array.array('L', [0] * (n + 1))


            for i in range(n):
                name = f.readline().strip()
                self._titles.append(name)
                (size, flag, num_links) = tuple(map(int, f.readline().strip().split()))
                self._redirect[i] = flag
                self._sizes[i] = size
                self._offset[i + 1] = self._offset[i] + num_links
                for j in range(num_links):
                    self._links[self._offset[i] + j] =  int(f.readline().strip())
        f.close()
        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        number = self._offset[_id + 1] - self._offset[_id]
        return number


    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id + 1]]

    def get_id(self, title):
        return self._titles.index(title)

    def get_number_of_pages(self):
        return self._num_of_pages

    def is_redirect(self, _id):
        if self._redirect[_id] == 1:
            return True
        else:
            return False

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]



def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл
def bfs(graph, start, finish):
    used = set()
    Q = [start]
    paths = {}
    paths[start] = [start]
    while Q:
        current = Q.pop(0)
        for neighbour in graph.get_links_from(current):
            if neighbour not in used:
                Q.append(neighbour)
                used.add(neighbour)
                paths[neighbour] = paths[current] + [neighbour]
            if neighbour == finish:
                return paths[neighbour]
    print('Путь не найден.')
    return
def statistics_wiki(graph):
    print('Введите старт и финиш.')
    start = input()
    finish = input()
    while start != 'break':
        print("Ищем путь от %s до %s. Запускаем обход в ширину" %(start, finish))
        print(*[graph.get_title(x) for x in bfs(graph, graph.get_id(start), graph.get_id(finish))])
        print('Введите старт и финиш.')
        start = input()
        finish = input()
    count_redir = 0
    for page in range(graph.get_number_of_pages()):
        if graph.is_redirect(page):
            count_redir += 1
    num_of_links = [graph.get_number_of_links_from(i) for i in range(graph.get_number_of_pages())]
    min_num_of_links = min(num_of_links)
    max_num_of_links = max(num_of_links)
    count_min_links = num_of_links.count(min_num_of_links)
    count_max_links = num_of_links.count(max_num_of_links)
    print('Количество статей с перенаправлением: %d (%0.2f%%)' % (count_redir, count_redir / graph.get_number_of_pages() * 100))
    print('Минимальное количество ссылок:', min_num_of_links)
    print('Количество статей с минимальным количеством ссылок:', count_min_links)
    print('Максимальное количество ссылок из статьи:', max_num_of_links)
    print('Количество статей с максимальным количеством ссылок:', count_max_links)
    print('Статья с наибольшим количеством ссылок:', graph.get_title(num_of_links.index(max_num_of_links)))
    print('Среднее количество ссылок в статье:','%0.2f (ср. откл. %0.2f)' %(statistics.mean(num_of_links), statistics.stdev(num_of_links)))
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

        # TODO: статистика и гистограммы
    statistics_wiki(wg)