function Follow (url) {
    $.post(url, $('#follow-user').serialize(), function (data) {
        if (data['followed'] === true) {
            const ButtonA = $('#follow-button')[0];
            ButtonA.className = 'unfollowing-user'
            ButtonA.style.display = 'inline-block';
            ButtonA.style.backgroundColor = 'black';
            ButtonA.style.cursor = 'pointer';
            ButtonA.style.color = 'white';
            ButtonA.innerHTML = '';
        } else {
            $.post(url.replace('follow', 'unfollow'), $('#follow-user').serialize(), function () {
                let ButtonB = $('#follow-button')[0];
                ButtonB.className = 'following-user';
                ButtonB.style.display = 'inline-block';
                ButtonB.style.backgroundColor = 'white';
                ButtonB.style.cursor = 'pointer';
                ButtonB.style.color = 'black';
                ButtonB.innerHTML = 'Follow'
            })
        }
    })
}

function Unfollow (url) {
    $.post(url, $('#unfollow-user').serialize(), function (data) {
        if (data['unfollowed'] === true) {
            const ButtonA = $('#unfollow-button')[0];
            ButtonA.className = 'following-user'
            ButtonA.style.display = 'inline-block';
            ButtonA.style.backgroundColor = 'white';
            ButtonA.style.cursor = 'pointer';
            ButtonA.style.color = 'black';
            ButtonA.innerHTML = 'Follow';
        } else {
            $.post(url.replace('unfollow', 'follow'), $('#unfollow-user').serialize(), function () {
                let ButtonB = $('#unfollow-button')[0];
                ButtonB.className = 'unfollowing-user';
                ButtonB.style.display = 'inline-block';
                ButtonB.style.backgroundColor = 'black';
                ButtonB.style.cursor = 'pointer';
                ButtonB.style.color = 'white';
                ButtonB.innerHTML = ''
            })
        }
    })
}