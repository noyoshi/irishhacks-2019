# Post.py

class Post:
    '''
    Class to represent a general post.
    '''

    def __init__(self, title, description, location,
                 skill_set, num_volunteers, is_request, tags=None):
        self.title = title
        self.description = description
        self.location = location
        self.skill_set = skill_set
        self.num_volunteers = num_volunteers
        self.is_request = is_request
        self.tags = tags

    def get_title(self):
        ''' returns title of post '''
        return self.title

    def set_title(self, title):
        ''' sets title of post '''
        self.title = title

    def get_description(self):
        ''' gets description of post '''
        return self.description

    def set_description(self, description):
        ''' sets description of post '''
        self.description = description

    def get_location(self):
        ''' gets location attached to post '''
        return self.location

    def set_location(self, location):
        ''' sets location of post '''
        self.location = location

    def get_skill_set(self):
        ''' returns skill set attached to post '''
        return self.skill_set

    def set_skill_set(self, skill_set):
        ''' sets skill set attached to post '''
        self.skill_set = skill_set

    def get_num_volunteers(self):
        ''' returns number of volunteers available/needed '''
        return self.num_volunteers
    
    def set_num_volunteers(self, num_volunteers):
        ''' sets number of volunteers needed/available '''
        self.num_volunteers = num_volunteers

    def get_is_request(self):
        ''' return if the post is a request '''
        return self.is_request

    def set_is_request(self, is_request):
        ''' sets if the post is a request '''
        self.is_request = is_request

    def get_tags(self):
        ''' gets tags from post '''
        return self.tags

    def set_tags(self, tags):
        ''' sets tags of post '''
        self.tags = tags

    def add_tag(self, tag):
        ''' add an additonal tag to post '''
        self.tags.append(tag)
