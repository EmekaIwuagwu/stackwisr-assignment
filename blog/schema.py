import graphene
from graphene_django import DjangoObjectType
from .models import Author, Post, Comment
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('id', 'name', 'email', 'bio')
        interfaces = (relay.Node,)

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author', 'comments')
        interfaces = (relay.Node,)

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'post')
        interfaces = (relay.Node,)

class Query(graphene.ObjectType):
    all_posts = DjangoFilterConnectionField(PostType)
    post = relay.Node.Field(PostType)
    all_authors = DjangoFilterConnectionField(AuthorType)
    author = relay.Node.Field(AuthorType)
    all_comments = DjangoFilterConnectionField(CommentType)
    comment = relay.Node.Field(CommentType)

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_all_authors(self, info, **kwargs):
        return Author.objects.all()

    def resolve_all_comments(self, info, **kwargs):
        return Comment.objects.all()

class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        bio = graphene.String(required=True)

    author = graphene.Field(AuthorType)

    def mutate(self, info, name, email, bio):
        author = Author(name=name, email=email, bio=bio)
        author.save()
        return CreateAuthor(author=author)

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, content, author_id):
        author = Author.objects.get(pk=author_id)
        post = Post(title=title, content=content, author=author)
        post.save()
        return CreatePost(post=post)

class CreateComment(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.ID(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, content, post_id):
        post = Post.objects.get(pk=post_id)
        comment = Comment(content=content, post=post)
        comment.save()
        return CreateComment(comment=comment)

class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
