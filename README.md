Secret Sharing
=============

A system for sharing secrets using Shamir's Secret Sharing Scheme.

## Sample Usage

#### Creating secrets from ascii strings

    >>> from secretsharing.shamir import Secret
    >>> secret = Secret.from_printable_ascii("Hello, world!")
    >>> secret.as_printable_ascii()
    'Hello, world!'
    >>> secret.as_int()
    43142121247394322427211362L

#### Create the same secret from an integer

    >>> secret = Secret(43142121247394322427211362L)

#### Spliting secrets into shares

    >>> shares = secret.split(3, 5)
    >>> print shares
    ['1-361480686792868891995835563', '2-143386489676856042916358664', '3-7829549542045912638342776', '4-573779886031128638611350010', '5-603297459858723945936256144']

#### Recovering secrets from shares

  	>>> recovered_shares = ['2-143386489676856042916358664', '3-7829549542045912638342776', '4-573779886031128638611350010']
    >>> recovered_secret = Secret.from_shares(recovered_shares)
    >>> recovered_secret.as_printable_ascii()
    'Hello, world!'

#### Shares too long? Use Bitcoin inspired base58 encoding instead of integers

    >>> from secretsharing.b58_shamir import b58Secret
    >>> secret = b58Secret.from_printable_ascii("Hello, world!")
    >>> b58_shares = secret.split(3, 5)
    >>> print b58_shares
    ['2-bJZZAcPPCEUbNdm', '3-8EfreFXbq2kyXwL', '4-wcT3haxPS87oV3T', '5-rU35Lm1VXwxqq7b', '6-33mHzZdMAc4tKxzH']

#### Recovering secrets from base58 shares

    >>> recovered_shares = ['3-8EfreFXbq2kyXwL', '4-wcT3haxPS87oV3T', '5-rU35Lm1VXwxqq7b']
    >>> recovered_secret = b58Secret.from_shares(recovered_shares)
    >>> print recovered_secret.as_printable_ascii()
    'Hello, world!'
