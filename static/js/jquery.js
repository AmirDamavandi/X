
$(document).ready(function () {
$('#tweet-submit').on('submit', function (e) {
    e.preventDefault();

    var formData = new FormData(this);

    $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            var tweetBox = $('#home-container .tweet-box')[0];
            $(tweetBox).after(data['rendered_tweet']);
            var tweetInput = $('#id_tweet')[0];
            tweetInput.value = '';
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
        }
    });
});
});

function LikeTweet(url) {
$.post(url, $('#like-tweet').serialize(), function (data) {
        if (data['is_liked'] === true) {
            let Form = $(`form[action="${url}"]`)[0];
            let flexBox = $(Form).parents('.flexbox')[0];
            let likeIcon = $(flexBox).find('.like-icon .line-icons-icon')[0];
            let likeCount = $(flexBox).find('.count3')[0];
            $(likeIcon).attr('src', '/static/twitter-icons/fill-heart.png');
            if (likeCount.innerText !== '') {
                likeCount.innerText = parseInt(likeCount.innerText) + 1;
                $(likeCount).css('color', 'rgb(235, 35, 128)');
            } else {
                likeCount.innerText = 1;
                $(likeCount).css('color', 'rgb(235, 35, 128)');

            }
        } else {
            $.post(url.replace('like', 'unlike'), $('#unlike-tweet').serialize(), function () {
                let Form = $(`form[action="${url}"]`)[0];
                let flexBox = $(Form).parents('.flexbox')[0];
                let likeIcon = $(flexBox).find('.like-icon .line-icons-icon')[0];
                let likeCount = $(flexBox).find('.count3')[0];
                $(likeIcon).attr('src', '/static/twitter-icons/heart.png');
                if (likeCount.innerText !== '1') {
                    likeCount.innerText = parseInt(likeCount.innerText) - 1;
                    $(likeCount).css('color', 'rgb(113, 118, 123)');
                } else {
                    likeCount.innerText = '';
                }
            });

        }
    });
}

function UnlikeTweet(url) {
$.post(url, $('#unlike-tweet').serialize(), function (data) {
    if (data['unliked'] === true) {
        let Form = $(`form[action="${url}"]`)[0];
        let flexBox = $(Form).parents('.flexbox')[0];
        let likeIcon = $(flexBox).find('.like-icon .line-icons-icon')[0];
        let likeCount = $(flexBox).find('.count3')[0];
        $(likeIcon).attr('src', '/static/twitter-icons/heart.png');
        if (likeCount.innerText !== '1') {
                likeCount.innerText = parseInt(likeCount.innerText) - 1;
                $(likeCount).css('color', 'rgb(113, 118, 123)');
            } else {
                likeCount.innerText = '';

            }

    } else {
        $.post(url.replace('unlike', 'like'), $('#like-tweet').serialize(), function () {
            let Form = $(`form[action="${url}"]`)[0];
            let flexBox = $(Form).parents('.flexbox')[0];
            let likeIcon = $(flexBox).find('.like-icon .line-icons-icon')[0];
            let likeCount = $(flexBox).find('.count3')[0];
            $(likeIcon).attr('src', '/static/twitter-icons/fill-heart.png');
            if (likeCount.innerText !== '') {
                likeCount.innerText = parseInt(likeCount.innerText) + 1;
                $(likeCount).css('color', 'rgb(235, 35, 128)');
            } else {
                likeCount.innerText = 1;
            }
        });
    }
});
}
function RetweetTweet(url) {
$.post(url, $('#retweet-tweet').serialize(), function (data) {
if (data['retweeted'] === true) {
    let Form = $(`form[action="${url}"]`)[0];
    let flexBox = $(Form).parents('.flexbox')[0];
    let likeIcon = $(flexBox).find('.retweet-icon .line-icons-icon')[0];
    let likeCount = $(flexBox).find('.count2')[0];
    $(likeIcon).attr('src', '/static/twitter-icons/repeated.png');
    if (likeCount.innerText !== '') {
        likeCount.innerText = parseInt(likeCount.innerText) + 1;
        $(likeCount).css('color', 'rgb(8, 219, 135)');
    } else {
        likeCount.innerText = 1;
        $(likeCount).css('color', 'rgb(8, 219, 135)');

    }
} else {
    $.post(url.replace('retweet', 'unretweet'), $('#unretweet').serialize(), function () {
        let Form = $(`form[action="${url}"]`)[0];
        let flexBox = $(Form).parents('.flexbox')[0];
        let likeIcon = $(flexBox).find('.retweet-icon .line-icons-icon')[0];
        let likeCount = $(flexBox).find('.count2')[0];
        $(likeIcon).attr('src', '/static/twitter-icons/repeat.png');
        if (likeCount.innerText !== '1') {
            likeCount.innerText = parseInt(likeCount.innerText) - 1;
            $(likeCount).css('color', 'rgb(113, 118, 123)');
        } else {
            likeCount.innerText = '';
        }
    });
}
});
}
function UnretweetTweet(url) {
    $.post(url, $('#unretweet').serialize(), function (data) {
    if (data['unretweeted'] === true) {
        let Form = $(`form[action="${url}"]`)[0];
        let flexBox = $(Form).parents('.flexbox')[0];
        let likeIcon = $(flexBox).find('.retweet-icon .line-icons-icon')[0];
        let likeCount = $(flexBox).find('.count2')[0];
        $(likeIcon).attr('src', '/static/twitter-icons/repeat.png');
        if (likeCount.innerText !== '1') {
                likeCount.innerText = parseInt(likeCount.innerText) - 1;
                $(likeCount).css('color', 'rgb(113, 118, 123)');
            } else {
                likeCount.innerText = '';

            }

    } else {
        $.post(url.replace('unretweet', 'retweet'), $('#retweet-tweet').serialize(), function () {
            let Form = $(`form[action="${url}"]`)[0];
            let flexBox = $(Form).parents('.flexbox')[0];
            let likeIcon = $(flexBox).find('.retweet-icon .line-icons-icon')[0];
            let likeCount = $(flexBox).find('.count2')[0];
            $(likeIcon).attr('src', '/static/twitter-icons/repeated.png');
            if (likeCount.innerText !== '') {
                likeCount.innerText = parseInt(likeCount.innerText) + 1;
                $(likeCount).css('color', 'rgb(8, 219, 135)');
            } else {
                likeCount.innerText = 1;
            }
        });
    }
});

}
