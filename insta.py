authors_usernames = [
    "giancarlomcosta",
    "eduardomahon",
    "stefaniesande",
    "ondejazzmeucoracao",
    "elisangela.saboia",
    "clarkmangabeira",
    "janelas.do.meu.quarto",
    "podeserpoema",
    "ananax666",
    "pachaana",
    "osolferreira",
    "laricampos10",
    "apoetriz",
]


def get_authors():
    for author in authors_usernames:
        author = Profile(author)
        yield author


class Post:
    def __init__(self, post_id, caption="", image_url="", likes=None, comments=None):
        self.post_id = post_id
        self.caption = caption
        self.image_url = image_url
        self.likes = likes
        self.comments = comments

    def __hash__(self) -> int:
        return hash(self.post_id)

    @property
    def post_url(self):
        return f"https://www.instagram.com/p/{self.post_id}/"


class Profile:
    def __init__(self, username: str, posts: set = None, author: bool = False):
        self.username = username
        self.posts = posts

    def __hash__(self) -> int:
        return hash(self.username)

    @property
    def profile_url(self):
        return f"https://www.instagram.com/{self.username}/"
