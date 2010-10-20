from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def admin (posts):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    self['title'] = join_(u'Blog Admin')
    extend_([u'\n'])
    extend_([u'<article>\n'])
    extend_([u'        <header>\n'])
    extend_([u'                <h2>Posts</h2>\n'])
    extend_([u'        </header>\n'])
    extend_([u'        <table id="admin_posts">\n'])
    extend_([u'                <thead>\n'])
    extend_([u'                <tr><td><input type="checkbox" id="check_all"></td><td>Title</td><td>Status</td><td>Date</td><td>Author</td></tr>\n'])
    extend_([u'                </thead>\n'])
    extend_([u'                <tbody>\n'])
    for post in loop.setup(posts):
        extend_(['                ', u'    <tr><td></td><td>', escape_(post.title, True), u'</td><td>', escape_(post.status, True), u'</td><td>', escape_(post.pubdate, True), u'</td><td>', escape_(post.author, True), u'</td><td><a href="/admin/edit/', escape_(post.key(), True), u'">edit</a></tr>    \n'])
    extend_([u'                </tbody>\n'])
    extend_([u'        </table>\n'])
    extend_([u'</article>\n'])
    extend_([u'\n'])
    extend_([u'<article>\n'])
    extend_([u'        <header>\n'])
    extend_([u'                <h2>Add Post</h2>\n'])
    extend_([u'        </header>\n'])
    extend_([u'        <p>\n'])
    extend_([u'                <form method="post" action="/post" id="admin_edit">\n'])
    extend_([u'                        <input type="text" name="title" /><br />\n'])
    extend_([u'                        <textarea name="content"></textarea><br />\n'])
    extend_([u'                        <button type="submit">save</button>\n'])
    extend_([u'                </form>\n'])
    extend_([u'        </p>\n'])
    extend_([u'</article>\n'])

    return self

admin = CompiledTemplate(admin, 'templates/admin.html')
join_ = admin._join; escape_ = admin._escape

# coding: utf-8
def archive (posts, when):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    self['title'] = join_(u'Nik Cubrilovic : Home')
    extend_([u'\n'])
    extend_([u'<h1>Archive for ', escape_(when, True), u'</h1>\n'])
    extend_([u'\n'])
    for post in loop.setup(posts):
        extend_([u'    <article> \n'])
        extend_([u'            <header> \n'])
        extend_([u'                    <time datetime="2009-10-17" pubdate>', escape_(post.date, True), u'</time> \n'])
        extend_([u'                    <h1> \n'])
        extend_([u'                            <a href="../semantics.html" rel="bookmark" title="link to this post">', escape_(post.title, True), u'</a> \n'])
        extend_([u'                    </h1> \n'])
        extend_([u'            </header> \n'])
        extend_([u'            <p>', escape_(post.content, False), u'</p>\n'])
        extend_([u'    </article>\n'])

    return self

archive = CompiledTemplate(archive, 'templates/archive.html')
join_ = archive._join; escape_ = archive._escape

# coding: utf-8
def base (page):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<!DOCTYPE html>\n'])
    extend_([u'<html lang="en" dir="ltr">\n'])
    extend_([u'<head>\n'])
    extend_([u'        <meta charset="utf-8">\n'])
    extend_([u'        <title>', escape_(page.title, True), u'</title>\n'])
    extend_([u'        <base href=".">\n'])
    extend_([u'        <meta name="application-name" content="">\n'])
    extend_([u'        <meta name="author" value="Nik Cubrilovic">\n'])
    extend_([u'        <meta name="description" value="Blog of Nik Cubrilovic">\n'])
    extend_([u'        <meta name="generator" value="Unicorn v0.1">\n'])
    extend_([u'        <link id="css-reset" rel="stylesheet" href="/css/reset.css" type="text/css">\n'])
    extend_([u'        <link id="css-core" rel="stylesheet" href="/css/style.css" type="text/css">\n'])
    extend_([u'        <link id="css-admin" rel="stylesheet" href="/css/admin.css" type="text/css">\n'])
    extend_([u'        <link id="feed-atom" rel="alternate" href="/feed" type="application/atom+xml" title="Nik Cubrilovic">\n'])
    extend_([u'        ', escape_(page.get('head'), False), u'\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u'<header>\n'])
    extend_([u'        <img src="/img/nik.png" border="0">\n'])
    extend_([u'    <h1><a href="/">Nik Cubrilovic</a></h1>      \n'])
    extend_([u'        <nav>\n'])
    extend_([u'                <ul>\n'])
    extend_([u'                        <li><a href="/admin">Admin</a></li>\n'])
    extend_([u'                        <li><a href="/about">About</a></li>\n'])
    extend_([u'                        <li><a href="/archive">Archive</a></li>\n'])
    extend_([u'                        <li><a href="/projects">Projects</a></li>\n'])
    extend_([u'                        <li><a href="/contact">Contact</a></li>\n'])
    extend_([u'                </ul>\n'])
    extend_([u'        </nav>\n'])
    extend_([u'</header>\n'])
    extend_([u'<aside>\n'])
    extend_([u'        <nav>\n'])
    extend_([u'                <ul>\n'])
    extend_([u'                        <li>Admin >> </li>\n'])
    extend_([u'                        <li><a href="/admin">Main</a></li>\n'])
    extend_([u'                        <li><a href="/admin">Posts</a></li>\n'])
    extend_([u'                        <li><a href="/admin">Comments</a></li>\n'])
    extend_([u'                </ul>\n'])
    extend_([u'        </nav>\n'])
    extend_([u'</aside>\n'])
    extend_([u'  ', escape_(page, False), u'\n'])
    extend_([u'<footer>\n'])
    extend_([u'        <p>&copy; 2010 Nik Cubrilovic</p>\n'])
    extend_([u'        <p>This is an html5 page</p>\n'])
    extend_([u'</footer>\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

base = CompiledTemplate(base, 'templates/base.html')
join_ = base._join; escape_ = base._escape

# coding: utf-8
def error (error):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    self['title'] = join_(u'Nik Cubrilovic : File Not Found')
    extend_([u'\n'])
    extend_([u'<article>\n'])
    extend_([u'        <header>\n'])
    extend_([u'                <h1>', escape_(error, True), u'</h1>\n'])
    extend_([u'        </header>\n'])
    extend_([u'</article>\n'])

    return self

error = CompiledTemplate(error, 'templates/error.html')
join_ = error._join; escape_ = error._escape

# coding: utf-8
def index (posts, path, login_url):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    self['title'] = join_(u'Nik Cubrilovic : Home')
    extend_([u'\n'])
    extend_([u'<h1>Path was ', escape_(path, True), u'</h1>\n'])
    for post in loop.setup(posts):
        extend_([u'    <article> \n'])
        extend_([u'            <header> \n'])
        extend_([u'                    <time datetime="2009-10-17" pubdate>', escape_(post.pubdate, True), u'</time> \n'])
        extend_([u'                    <h1> \n'])
        extend_([u'                            <a href="/', escape_(post.key, True), u'" rel="bookmark" title="', escape_(post.title, True), u'">', escape_(post.title, True), u'</a> \n'])
        extend_([u'                            by ', escape_(post.author, True), u'\n'])
        extend_([u'                    </h1> \n'])
        extend_([u'            </header> \n'])
        extend_([u'            <p>', escape_(post.content, False), u'</p>\n'])
        extend_([u'    </article>\n'])
        extend_([u'\n'])

    return self

index = CompiledTemplate(index, 'templates/index.html')
join_ = index._join; escape_ = index._escape

# coding: utf-8
def server_error():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<!DOCTYPE html>\n'])
    extend_([u'<html lang="en" dir="ltr">\n'])
    extend_([u'<head>\n'])
    extend_([u'        <meta charset="utf-8">\n'])
    extend_([u'        <title>Error</title>\n'])
    extend_([u'        <base href=".">\n'])
    extend_([u'        <meta name="application-name" content="">\n'])
    extend_([u'        <meta name="author" value="Nik Cubrilovic">\n'])
    extend_([u'        <meta name="description" value="Blog of Nik Cubrilovic">\n'])
    extend_([u'        <meta name="generator" value="Unicorn v0.1">\n'])
    extend_([u'        <link id="css-reset" rel="stylesheet" href="/css/reset.css" type="text/css">\n'])
    extend_([u'        <link id="css-core" rel="stylesheet" href="/css/style.css" type="text/css">\n'])
    extend_([u'        <link id="css-admin" rel="stylesheet" href="/css/admin.css" type="text/css">\n'])
    extend_([u'        <link id="feed-atom" rel="alternate" href="/feed" type="application/atom+xml" title="Nik Cubrilovic">\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u'<header>\n'])
    extend_([u'        <img src="/img/nik.png" border="0">\n'])
    extend_([u'    <h1><a href="/">Nik Cubrilovic</a></h1>      \n'])
    extend_([u'        <nav>\n'])
    extend_([u'                <ul>\n'])
    extend_([u'                        <li><a href="/admin">Admin</a></li>\n'])
    extend_([u'                        <li><a href="/about">About</a></li>\n'])
    extend_([u'                        <li><a href="/archive">Archive</a></li>\n'])
    extend_([u'                        <li><a href="/projects">Projects</a></li>\n'])
    extend_([u'                        <li><a href="/contact">Contact</a></li>\n'])
    extend_([u'                </ul>\n'])
    extend_([u'        </nav>\n'])
    extend_([u'</header>\n'])
    extend_([u'<aside>\n'])
    extend_([u'        <nav>\n'])
    extend_([u'                <ul>\n'])
    extend_([u'                        <li>Admin >> </li>\n'])
    extend_([u'                        <li><a href="/admin">Main</a></li>\n'])
    extend_([u'                        <li><a href="/admin">Posts</a></li>\n'])
    extend_([u'                        <li><a href="/admin">Comments</a></li>\n'])
    extend_([u'                </ul>\n'])
    extend_([u'        </nav>\n'])
    extend_([u'</aside>\n'])
    extend_([u'<article>\n'])
    extend_([u'        <header>\n'])
    extend_([u'                <h1>500 - Server Error</h1>\n'])
    extend_([u'        </header>\n'])
    extend_([u'        <p>An error has occured</p>\n'])
    extend_([u'</article>\n'])
    extend_([u'<footer>\n'])
    extend_([u'        <p>&copy; 2010 Nik Cubrilovic</p>\n'])
    extend_([u'        <p>This is an html5 page</p>\n'])
    extend_([u'</footer>\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

server_error = CompiledTemplate(server_error, 'templates/server_error.html')
join_ = server_error._join; escape_ = server_error._escape

