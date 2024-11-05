$(document).ready(function () {
    // Initially hide all child nodes
    $('.genealogy-tree ul').hide();
    // Show only the top-level nodes
    $('.genealogy-tree > ul').show();

    // Event listener for clicking on list items
    $('.genealogy-tree li').on('click', function (e) {
        var children = $(this).children('ul');
        if (children.is(':visible')) {
            children.hide('fast').removeClass('active');
        } else {
            children.show('fast').addClass('active');
        }
        e.stopPropagation();  // Prevent event from bubbling up
    });
});