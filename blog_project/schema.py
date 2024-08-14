import graphene
from graphene_django import DjangoObjectType
from blog.models import Author, Post, Comment
import graphql_jwt

# Define GraphQL types for each of your models
class AuthorType(DjangoObjectType):
    class Meta:
        model = Author

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

# Define mutations for creating authors, posts, and comments
class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    author = graphene.Field(AuthorType)

    def mutate(self, info, name, email):
        author = Author(name=name, email=email)
        author.save()
        return CreateAuthor(author=author)

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.Int(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, content, author_id):
        author = Author.objects.get(id=author_id)
        post = Post(title=title, content=content, author=author)
        post.save()
        return CreatePost(post=post)

class CreateComment(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.Int(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, content, post_id):
        post = Post.objects.get(id=post_id)
        comment = Comment(content=content, post=post)
        comment.save()
        return CreateComment(comment=comment)

# Define the Query class
class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    all_posts = graphene.List(PostType)
    all_comments = graphene.List(CommentType)

    def resolve_all_authors(self, info):
        return Author.objects.all()

    def resolve_all_posts(self, info):
        return Post.objects.all()

    def resolve_all_comments(self, info):
        return Comment.objects.all()

# Define the Mutation class to handle both model mutations and JWT authentication
class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# Define the schema with both Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
