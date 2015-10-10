Project proposal feedback
==================

**Team number**: 142
**Team name**: Code Challenge!
**Team members**: [haileiy, jiaxix, jli3]

### Paul

I think it is definitely possible with a group of your size to not only accomplish this project, but go beyond your general proposal to perhaps consider using different APIs like Google Hangout to coordinate live coding mock interviews, for example, within your website. Also, definitely checkout PrismJS which can do syntax highlighting for you. When you think about your definite specifications, make sure that there is enough work for all of you to demonstrate your knowledge of course concepts--I think this is possible, as long as you branch out a bit. I like the idea a lot!

### Andrew

I'd be REALLY careful with this, as while you'll be 100% safe when developing locally, you'll eventually need to implement some sort of sandboxing (along with the expected features in a sandbox like timeouts, etc.). If you don't and some prospective spammer/malicious user finds your site you may end up getting service removed by your web hosting service (AWS, Heroku, whoever you choose). You may want to look into https://github.com/openjudge/sandbox as it suports C/C++ and Python, which is more than enough for you to get started. Another possibility is to just compile everything to Javascript (basically everything compiles to Javascript, you just need the right library) as this will allow clients to test their code client side to see if it's legal (no non-sandboxed libraries) and you can verify with random inputs or something or have the community "verify" it by upvote/downvote, so shift the focus less from an online judge to more like ProjectEuler and CodeGolf.

### Shuai

Your project idea is interesting and practical. While it meets a lot of the course learning goals, I would suggest you to go further by extending your features to use appropriate APIs. For example, Prism.js would be helpful for syntax highlighting in your code editor. Also, it looks like you would need a file storage system for testing modules on your backend. I would recommend using a remote storage like Amazon S3. You should also propose what database you prepare to use.



---

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/142/blob/master/feedback/proposal.md