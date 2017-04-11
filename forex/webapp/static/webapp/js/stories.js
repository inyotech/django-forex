function show_stories() {
    console.log('stories', stories)
    story_elements = [];
    $.each(stories.data, function(i, s) {
        console.log(s);
        story_elements.push('<div><a href="' + s.link + '">' + s.title + '</a><br/>' + s.description + '</div>');
    });
    $('#news').html(story_elements.join(''));
}
