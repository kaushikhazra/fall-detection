document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('myModal');
    const videoPlayer = document.getElementById('video-player');
    const closeBtn = document.getElementsByClassName('close')[0];

    document.querySelectorAll('.thumbnail').forEach(item => {
        item.addEventListener('click', event => {
            const videoSrc = item.getAttribute('data-video-src');
            videoPlayer.src = videoSrc;
            modal.style.display = 'block';
            videoPlayer.play();  // Auto play the video
        });
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        videoPlayer.pause();
        videoPlayer.src = '';
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            videoPlayer.pause();
            videoPlayer.src = '';
        }
    });
});
