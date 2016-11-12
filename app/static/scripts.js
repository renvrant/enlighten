'use strict';

function initPage() {
  $('.comment .comment-form').hide();
  $('.hide-reply-form').hide();
}

function toggleReplyForm(event) {
  event.preventDefault();
  const button = $(event.target);
  $('.comment .comment-form').hide();
  ['.comment-form', '.hide-reply-form'].map((selector) => {
    button
      .parent()
      .parent()
      .find(selector)
      .show();
  });
}

function hideCommentForm(event) {
  $('.comment .comment-form').hide();
  $('.hide-reply-form').hide();
}

$(document).ready(() => {
  // INIT
  initPage();

  // Event Listeners
  $('.toggle-reply-form').on('click', toggleReplyForm);
  $('.hide-reply-form').on('click', hideCommentForm);
});
