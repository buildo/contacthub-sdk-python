.. _authentication:

Authentication
==============

You can create a `Workspace` object that allows the control of the workspace's nodes. It require the workspace id and
the access token provided by ContactHub::


    my_workspace = Workspace(workspace_id='workspace_id', token='token')

If not specified, the SDK will use the default URL for the ConctactHub API - `https://api.contactlab.it/hub/v1` - but
you can specify a different base URL for the API::

    my_workspace = Workspace(workspace_id='workspace_id', token='token', base_url='base_url')

Once obtained a workspace, you're able to access the various nodes linked to it with the `get_node` method::

    node = workspace.get_node(node_id='node_id')


This method will return a `Node` object, that allows you to perform all operations on customers and events.
A ``Node`` is a key object for getting, posting, putting, patching and deleting data on entities.

Authenticating via configuration file
-------------------------------------

You can specify the workspace ID, the access token and the base url (not mandatory. If ommited, the default base URL for ContactHub will be used)
via INI file::

    my_workspace = Workspace.from_INI_file('file.INI')


The file must follow this template::

    workspace_id = workspace_id
    token = token
    base_url = base_url

Proxies
-------
If you need to use a proxy, you can configure requests by setting the environment variables HTTP_PROXY and HTTPS_PROXY::

    $ export HTTP_PROXY="http://10.10.1.10:3128"
    $ export HTTPS_PROXY="http://10.10.1.10:1080"

To use HTTP Basic Auth with your proxy, use the *http://user:password@host/* syntax::

    $ export HTTPS_PROXY="http://user:pass@10.10.1.10:3128/"

