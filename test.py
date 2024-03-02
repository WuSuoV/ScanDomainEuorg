import itertools

if __name__ == '__main__':
    f = open('./zidian.txt', 'w', encoding='utf-8')
    zimu = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    result = []
    for a, b in itertools.product(zimu, zimu):
        result.append(f'{a}{b}{a}{b}')

    f.write('\n'.join(result))
    f.close()
