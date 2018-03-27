def save_comment(sender, instance, created, **kwargs):
    if created:
        comment = instance
        snippet = comment.snippet
        snippet.comment_count = snippet.comments.count()
        snippet.save(force_update=True)