const realData =
  'x2miSdXCrkYVOJHgspRuVXMo7uYE9jYZE8VVHRt2Lc5mo8NxxzGD3aiZrtF+lz1p/p0dTqek/J7f+9anER7ndar7ynXRqWJONdLaJHDNE+cUIYjFtnTBWfzHHPJcMjJevH5aeHR2B5yvNj24+xA8M+mpKtFjqURhiQHnwkg6Gy2kq3lt8RWdB/WI6yuHivJaGIQqqwcknTRBDdTSemnriIokF/ijImIX5B+YtoAqYQW+hKv5X68KkgIO0uBm1ug4+ZeZPwizBGybAQroiiTYWESSSV8ZdzXrgToY5oImQZBs1FwQj7yjEw7Z4LcXyAq6JDugOg/9EGcp+wq+yVdLTlR1a35qG77kDyQP+T2+kf73nxjWc7zIZyZDp680O4VQ55ORTESyHH7W+4Gs76XWXMm1Ua5896UNlFEyWNKQ1yZ2OgZgo8pErssVTPr0Z+cx9Sk4nch4soMSFfKowgy/DYHc++8YvaCxmBxYXhzauyqI9nGzfrm4CxBZHilVW0FdshgOUmbiFfGYycdKADIZt08niwiLXE3s2PG2e+5NfIa/HbdR4iwXZu9V0Z4sUXiRydGC9lsaOuPL2PxyJ++5r9ZMYDA+gIyatPFnisE+oqlElm1GAoee5uWEMINhPjlQQJkU7wihQ1B/dFiWcCN4/BSL0KnRPap3XamhKS9CP9hQ6hdgDELq4cEv/bHmv4c5ocB0u+H3ixSO6WIOihX9sLurzzYcJn2DfUP5O9bsBVfMxHPBAMsU+UsE8C87agUzesw8V3y1cazxR/glYCUKFbOqLy0wRvFH7VC6woJPOFQS9iI/PwJy9u/Shf0+IfO0//syaKZ2LFVuREoLHoHIlI3GQjmeElWz8URdHCwzrQfD4P2r+Ua5GLXemaBOYlV+XZtnFDed9QkXj1LNnK3CZ+sTszFRIuqgRQHznKuwtNqLbn3qSHffXQV8MsIE6yBpbc/fVEBWwUO8kGsuXeykvRwu2g+BIxZYusxEDOSxvQma9V/95U5O5irw9fypSGmR2JcBKhfTaTm1lFMyqF8S5A7/HefRtUW0vFj8w77+0MUaE5bOVIyPeMdlO6ZlgnxDf+KJ1G+4YyVLoPprllfV6rk5bMjhFKsgirpob7J79EqjvFh4yMCDD7dTySoLogTMHhT5/y+OdqbRIt9mTvXM3xb368PXMasbx3IcI6hBCMQwPNP8tcGMvsVwaiQaJtvkou279T3t5idBOr5KrGIroW1rLRqHZCbnlmwyrWzFmbeiNAhUiBOMV44bcLsudyqhOQEFeO/1/ta0zfzJQtk6j01X7gFVzdMzXHq33JXPIo0BF5URDj7IlKGduNPFBqLs5OM30LsJ7p+FtZYzLmZ+XdJ1chg+xHbEAyRegeQMNMA1JhzA9+6Ye78BzdOvIZ7vtUcoj39E6I0XOPEms8CHHsfEF6+JLCIoZBUTtRQtLsE4eKlZyFFnJodbijvvUMtmAgo+8B+WgEmkI9/4pFNqRPNGgVL9bPxtHItDhiH0EqAdoggCfN1KHiKup9yzxJT7jUCS1ucMYDqXHVPScDB7nw=='
module.exports = (query, request) => {
  query.cookie.os = 'pc'
  //sessiondId和rawdata需要客户端传进来
  const data = {
    algorithmCode: 'shazam_v2',
    times: 2,
    decrypt: 1,
    sessionId: 'a550ef7f-3894-4fc2-9bca-873b3acaeeb2',
    duration: 6,
    rawdata: realData,
  }
  return request(
    'POST',
    `https://interface.music.163.com/api/music/audio/match`,
    data,
    {
      crypto: 'api',
      cookie: query.cookie,
      proxy: query.proxy,
      realIP: query.realIP,
    },
  )
}
