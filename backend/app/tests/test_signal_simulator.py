from __future__ import annotations

import numpy as np
import pytest

from app.acquisition.simulator import BiosignalSimulator


@pytest.fixture
def simulator():
    return BiosignalSimulator(duration_s=10.0, tick_interval_ms=100, rng=np.random.default_rng(42))


class TestBiosignalSimulator:
    @pytest.mark.asyncio
    async def test_emits_window(self, simulator):
        await simulator.start()
        window = await simulator.get_window()
        await simulator.stop()
        assert window.modality == "multimodal"
        assert len(window.channel_names) == 18
        assert len(window.data) == 18

    @pytest.mark.asyncio
    async def test_channel_names(self, simulator):
        await simulator.start()
        window = await simulator.get_window()
        await simulator.stop()
        assert "Fp1" in window.channel_names
        assert "HR" in window.channel_names
        assert "gaze_x" in window.channel_names
        assert "blink" in window.channel_names

    @pytest.mark.asyncio
    async def test_data_shape(self, simulator):
        await simulator.start()
        window = await simulator.get_window()
        await simulator.stop()
        n_samples = int(round(250.0 * 0.1))
        for ch_data in window.data:
            assert len(ch_data) == n_samples

    @pytest.mark.asyncio
    async def test_multiple_windows(self, simulator):
        await simulator.start()
        for _ in range(5):
            w = await simulator.get_window()
            assert len(w.data) == 18
        await simulator.stop()

    @pytest.mark.asyncio
    async def test_not_running_raises(self, simulator):
        with pytest.raises(RuntimeError):
            await simulator.get_window()

    @pytest.mark.asyncio
    async def test_sqi_hint_present(self, simulator):
        await simulator.start()
        w = await simulator.get_window()
        await simulator.stop()
        assert w.signal_quality_hint is not None
        assert 0 <= w.signal_quality_hint <= 1
