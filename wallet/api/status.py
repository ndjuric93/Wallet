from wallet.api import api


@api.route('/status', methods=['GET'])
def get_status():
    """
    Returns status.

    :return: JSON status representation
    """
    return {
        'status': 'ok',
        'app': 'wallet'
    }
