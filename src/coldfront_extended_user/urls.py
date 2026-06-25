# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, path

from coldfront.registry import get_model_urls

from . import views  # noqa F401

app_name = "users"
urlpatterns = [
    path("users/<int:pk>/", include(get_model_urls("users", "user"))),
]