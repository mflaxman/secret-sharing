from shamir import Secret

from characters import int_to_b58, b58_to_int


class b58Secret(Secret):

    def point_to_share(self, point):
        if isinstance(point, tuple) and len(point) == 2:
            if isinstance(point[0], (int, long)):
                if isinstance(point[1], (int, long)):
                    x, y = point
                    if x > 255:
                        msg = 'The largest x coordinate for a share is 255.'
                        raise ValueError(msg)

                    return '%s-%s' % (int_to_b58(x), int_to_b58(y))

        raise ValueError('Point format is invalid. Must be integer pair.')

    def share_to_point(self, share):
        '''
        share should be in the format:
          `2-3AwSUjLj59...` for b58
        '''
        if isinstance(share, str) and share.count('-') == 1:
            x, y = share.split('-')
            return b58_to_int(x), b58_to_int(y)
        raise ValueError('Share format is invalid.')
