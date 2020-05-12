from flask import Flask, Response, request

app = Flask(__name__)


def get_test(test_id):
    source = open('tests/%s.txt' % test_id, encoding='utf-8').read()

    theme = source.split('\n')[1]
    tasks = source.split('\n\n')[1:]
    code_builder = []
    code_builder.append(f'''\
<h2>{theme}</h2>
<form name="test" method="post" action="/test_res/{test_id}">
<br>
''')

    for i, task in enumerate(tasks):
        t_type, text, answer = task.split('\n')
        if t_type == 'v':
            code_builder.append(f'''\
<p><b>{text}</b><br>
{''.join(f'<input type="radio" name="{i}" value="{val}">{val}<br>' for val in answer.split(': ')[1].split('; '))}
</p>''')
        elif t_type == 's':
            code_builder.append(f'''\
<p><b>{text}</b><br>
<input type="text" name="{i}" size=40>
</p>''')


    code_builder.append('''\
<p>
<br>
<input type="submit" value="Отправить"><br>
</p>''')
    code_builder.append('</form>')

    return ''.join(code_builder)


def get_test_answers(test_id):
    source = open('tests/%s.txt' % test_id, encoding='utf-8').read()

    tasks = source.split('\n\n')[1:]
    answers = []
    for task in tasks:
        t_type, text, answer = task.split('\n')
        if t_type == 's':
            answers.append(answer)
        elif t_type == 'v':
            i_id, answer = answer.split(': ')
            answers.append(answer.split('; ')[int(i_id) - 1])
    return answers


def get_subject(subj_id):
    return 'Yooh!'


@app.route('/')
def root():
    return open('html/main.html', encoding='utf-8').read()


@app.route('/test/<smth>')
def test(smth):
    tst = get_test(smth)
    return open('html/test.html', encoding='utf-8').read().replace('<include>', tst)


@app.route('/test_res/<t_id>', methods=['POST'])
def test_res(t_id):
    answers = dict(request.values)
    correct = get_test_answers(t_id)
    count = 0
    print(answers)
    print(correct)
    for i, correct_v in enumerate(correct):
        if not str(i) in answers:
            continue
        if answers[str(i)] == correct_v:
            count += 1
    return open('html/test_finish.html', encoding='utf-8').read().replace('<include>', str(f'{count}/{len(correct)}'))


@app.route('/subject/<subj>')
def subject(subj):
    sbj = get_subject(subj)
    return open('html/subject.html', encoding='utf-8').read().replace('<include>', sbj)


@app.route('/style/<filename>')
def css(filename):
    if '..' in filename:
        return
    print('filename', filename)
    info = open('style/' + filename, encoding='utf-8').read()
    info = info.replace('#222222', '#000000').replace('#333333', '#999999')
    return Response(info, mimetype='text/css', status=200)


@app.route('/api')
def api_main():
    pass


app.run('0.0.0.0', 28901)
