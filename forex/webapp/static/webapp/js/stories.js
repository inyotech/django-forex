function show_stories() {
    story_elements = [];
    $.each(stories.data, function(i, s) {
        story_elements.push('<div><a href="' + s.link + '">' + s.title + '</a><br/>' + s.description + '</div>');
    });
    $('#news').append(story_elements.join(''));
}
