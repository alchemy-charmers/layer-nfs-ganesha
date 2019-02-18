#!/usr/bin/python3


class TestLib():
    def test_pytest(self):
        assert True

    def test_nfsganesha(self, nfsganesha):
        ''' See if the helper fixture works to load charm configs '''
        assert isinstance(nfsganesha.charm_config, dict)

    # Include tests for functions in lib_nfs_ganesha
