import imp

import mock


class TestActions():
    def test_restart_action(self, nfsganesha, monkeypatch):
        mock_function = mock.Mock()
        monkeypatch.setattr(nfsganesha,
                            'restart_service',
                            mock_function)
        assert mock_function.call_count == 0
        imp.load_source('restart_service',
                        './actions/restart')
        assert mock_function.call_count == 1

    def test_reload_action(self, nfsganesha, monkeypatch):
        mock_function = mock.Mock()
        monkeypatch.setattr(nfsganesha,
                            'reload_config',
                            mock_function)
        assert mock_function.call_count == 0
        imp.load_source('reload_config',
                        './actions/reload')
        assert mock_function.call_count == 1
