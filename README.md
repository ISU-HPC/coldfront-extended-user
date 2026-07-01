# Coldfront Extended User Plugin

This plugin extends the core user model to support custom fields.

## Installation

Download the code or clone the repository. 

You can directly install the plugin via `uv pip`:

```
$ uv pip install .../coldfront-extended-user/
```

Next, add the plugin to the `PLUGINS` setting in your ColdFront configuration:
```
PLUGINS="coldfront_extended_user"
```

Lastly, migrate your DB:
```
$ uv run coldfront migrate
```

## Creating Custom User Fields

Custom user fields can be created just like other custom fields (e.g., the custom fields for allocations). When creating a custom field, select `Coldfront Extended USer > Custom User Field` for the Object Type.

## Viewing and Editing Custom User Fields

Elements to view and edit the custom fields have been injected directly into the core user views. When viewing individual user details, a `Custom Fields` card should appear in the bottom right.

**NOTE**: This card will NOT appear if you have not created any custom user fields.

A new button labeled `Edit User Fields` in the top right has also been added. This will direct you to a new page where you can edit and save custom user fields.

If you would like to add a tab to edit custom user fields, some code has been left in `src/view.py`.

## Accessing Custom Fields via API

The custom fields for all users can be accessed via the REST API via the following endpoint:

```
/api/plugins/coldfront_extended_user/custom-user-fields/
```

Each entry contains a nested user entry (which contains name, username, email, etc.) and the custom fields for that user.

To get the custom fields for a given user, use the following endpoint:

```
/api/plugins/coldfront_extended_user/custom-user-fields/user/{uid}/
```

## License
This plugin has been released under the MIT license.
