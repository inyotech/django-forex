function show_stories() {
    story_elements = [];
    $.each(stories.data, function(i, s) {
        story_elements.push('<p><a href="' + s.link + '">' + s.title + '</a><br/>' + s.description + '</p>');
    });
    $('#news').append(story_elements.join(''));
}
